"""Business logic for test execution - separated from UI.

Async-first design for responsive testing with proper error handling.
"""

import asyncio
import importlib.util
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

from gui.components.test_config import TestDataConfig


class TestExecutor:
    """Execute agent tests with async support and proper error handling."""
    
    def __init__(self):
        """Initialize test executor."""
        self.examples_dir = Path(__file__).parent.parent.parent / "examples"
    
    async def execute_test_async(
        self,
        agent_info: Dict,
        test_config: TestDataConfig,
        data: Optional[Dict]
    ) -> Dict:
        """Execute agent test asynchronously.
        
        Args:
            agent_info: Agent information dict
            test_config: Test configuration
            data: Prepared test data
            
        Returns:
            Test result dictionary
        """
        agent_path = self.examples_dir / agent_info["filename"]
        
        if not agent_path.exists():
            return {
                "success": False,
                "error": f"Agent file {agent_info['filename']} not found"
            }
        
        try:
            # Load agent module
            agent_class = await self._load_agent_async(
                agent_path,
                agent_info["name"]
            )
            
            if not agent_class:
                return {
                    "success": False,
                    "error": f"Agent class '{agent_info['name']}' not found in file"
                }
            
            # Create agent instance
            agent = agent_class()
            
            # Check if RAG agent
            is_rag_agent = self._is_rag_agent(agent)
            
            if is_rag_agent and test_config.uploaded_file:
                # RAG agent with document
                return await self._test_rag_agent_async(
                    agent,
                    test_config.ticker,
                    test_config.uploaded_file
                )
            elif is_rag_agent:
                return {
                    "success": False,
                    "error": "RAG agent requires a PDF document to analyze"
                }
            
            # Financial agent - prepare data
            if not data:
                data = await self._fetch_database_data_async(test_config.ticker)
            
            if not data:
                return {
                    "success": False,
                    "error": f"No data available for {test_config.ticker}"
                }
            
            # Execute analysis with timeout
            start_time = time.time()
            
            try:
                signal = await asyncio.wait_for(
                    agent.analyze(test_config.ticker, data),
                    timeout=30.0  # 30 second timeout
                )
            except asyncio.TimeoutError:
                return {
                    "success": False,
                    "error": "Analysis timed out after 30 seconds",
                    "error_type": "timeout"
                }
            
            execution_time = time.time() - start_time
            
            # Check for LLM fallback
            is_fallback = self._detect_llm_fallback(signal)
            llm_error_info = None
            
            if is_fallback:
                llm_error_info = self._parse_llm_error(signal.reasoning)
            
            return {
                "success": True,
                "signal": {
                    "direction": signal.direction,
                    "confidence": signal.confidence,
                    "reasoning": signal.reasoning,
                },
                "execution_time": execution_time,
                "ticker": test_config.ticker,
                "is_fallback": is_fallback,
                "llm_error_info": llm_error_info,
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            # Clean up imported module
            if "test_agent_module" in sys.modules:
                del sys.modules["test_agent_module"]
    
    async def _load_agent_async(self, agent_path: Path, agent_name: str):
        """Load agent class asynchronously.
        
        Args:
            agent_path: Path to agent file
            agent_name: Name of agent class
            
        Returns:
            Agent class or None
        """
        # Run module loading in executor to avoid blocking
        loop = asyncio.get_event_loop()
        
        def load_module():
            spec = importlib.util.spec_from_file_location("test_agent_module", agent_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["test_agent_module"] = module
            spec.loader.exec_module(module)
            return module
        
        module = await loop.run_in_executor(None, load_module)
        
        # Find agent class
        return self._find_agent_class(module, agent_name)
    
    def _find_agent_class(self, module, agent_class_name: Optional[str]):
        """Find Agent class in module.
        
        Args:
            module: Python module
            agent_class_name: Optional specific class name
            
        Returns:
            Agent class or None
        """
        from agent_framework import Agent
        
        if agent_class_name:
            # Look for specific class
            return getattr(module, agent_class_name, None)
        
        # Find first Agent subclass
        for name in dir(module):
            obj = getattr(module, name)
            if (isinstance(obj, type) and 
                issubclass(obj, Agent) and 
                obj is not Agent):
                return obj
        
        return None
    
    def _is_rag_agent(self, agent) -> bool:
        """Check if agent is RAG-powered.
        
        Args:
            agent: Agent instance
            
        Returns:
            True if RAG agent
        """
        return (
            hasattr(agent, "config") and
            agent.config and
            hasattr(agent.config, "rag") and
            agent.config.rag is not None
        )
    
    async def _test_rag_agent_async(self, agent, ticker: str, uploaded_file) -> Dict:
        """Test RAG agent with PDF document asynchronously.
        
        Args:
            agent: RAG agent instance
            ticker: Ticker symbol
            uploaded_file: Streamlit uploaded file
            
        Returns:
            Test result dict
        """
        try:
            from PyPDF2 import PdfReader
            
            # Extract text from PDF (async)
            loop = asyncio.get_event_loop()
            
            def extract_text():
                pdf_reader = PdfReader(uploaded_file)
                document_text = ""
                pages_with_text = 0
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    
                    if page_text and len(page_text.strip()) > 50:
                        document_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                        pages_with_text += 1
                
                return document_text, pages_with_text, len(pdf_reader.pages)
            
            document_text, pages_with_text, total_pages = await loop.run_in_executor(
                None, extract_text
            )
            
            # Validate extracted text
            if not document_text.strip():
                return {
                    "success": False,
                    "error": "No text could be extracted from PDF. This PDF may be a scanned image."
                }
            
            if len(document_text.strip()) < 100:
                return {
                    "success": False,
                    "error": f"Insufficient text extracted ({len(document_text)} chars). Try a different document."
                }
            
            # Run analysis with timeout
            start_time = time.time()
            
            try:
                signal = await asyncio.wait_for(
                    agent.analyze(ticker, document_text),
                    timeout=60.0  # 60 second timeout for RAG (longer processing)
                )
            except asyncio.TimeoutError:
                return {
                    "success": False,
                    "error": "Document analysis timed out after 60 seconds",
                    "error_type": "timeout"
                }
            
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "signal": {
                    "direction": signal.direction,
                    "confidence": signal.confidence,
                    "reasoning": signal.reasoning,
                    "insights": getattr(signal, "metadata", {}).get("insights", [])
                },
                "execution_time": execution_time,
                "ticker": ticker,
                "document_stats": {
                    "pages": total_pages,
                    "pages_with_text": pages_with_text,
                    "text_length": len(document_text)
                }
            }
            
        except ImportError:
            return {
                "success": False,
                "error": "PyPDF2 not installed. Run: pip install PyPDF2"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing PDF: {str(e)}"
            }
    
    async def _fetch_database_data_async(self, ticker: str) -> Optional[Dict]:
        """Fetch data from database asynchronously.
        
        Args:
            ticker: Ticker symbol
            
        Returns:
            Data dictionary or None
        """
        # Import database
        from agent_framework import Database, Config
        
        # Create database connection
        db = Database(Config.get_database_url())
        
        try:
            # Connect and fetch
            await db.connect()
            data = await db.get_fundamentals(ticker)
            await db.disconnect()
            
            return data
            
        except Exception as e:
            # Ensure cleanup
            try:
                await db.disconnect()
            except:
                pass
            
            return None
    
    def _detect_llm_fallback(self, signal) -> bool:
        """Detect if signal is from LLM fallback.
        
        Args:
            signal: Signal object
            
        Returns:
            True if fallback detected
        """
        reasoning = signal.reasoning.lower()
        
        fallback_indicators = [
            "llm error",
            "llm service unavailable",
            "fallback",
            "api error",
            "connection failed",
            "model not found"
        ]
        
        return any(indicator in reasoning for indicator in fallback_indicators)
    
    def _parse_llm_error(self, reasoning: str) -> Dict:
        """Parse LLM error information from reasoning.
        
        Args:
            reasoning: Signal reasoning text
            
        Returns:
            Error info dict
        """
        reasoning_lower = reasoning.lower()
        
        if "package not installed" in reasoning_lower or "import" in reasoning_lower:
            return {
                "error_type": "missing_package",
                "description": "Required LLM package not installed"
            }
        
        if "model not found" in reasoning_lower or "not downloaded" in reasoning_lower:
            return {
                "error_type": "model_not_found",
                "description": "LLM model not available"
            }
        
        if "connection" in reasoning_lower or "connect" in reasoning_lower:
            return {
                "error_type": "connection_error",
                "description": "Cannot connect to LLM service"
            }
        
        if "api key" in reasoning_lower:
            return {
                "error_type": "missing_api_key",
                "description": "API key not configured"
            }
        
        if "rate limit" in reasoning_lower:
            return {
                "error_type": "rate_limit",
                "description": "Rate limit exceeded"
            }
        
        return {
            "error_type": "unknown",
            "description": "LLM service error"
        }
