"""Agent Tester - Test agents with mock or real data and PDF documents"""

import sys
import importlib.util
import time
import asyncio
from pathlib import Path
from typing import Dict, Optional, Any


class AgentTester:
    """Test agents with mock, database data, or PDF documents."""

    def test_agent(
        self,
        agent_filename: str,
        ticker: str,
        mock_data: Optional[Dict] = None,
        uploaded_file: Optional[Any] = None,
        agent_class_name: Optional[str] = None,
    ) -> Dict:
        """Test an agent with provided data.

        Args:
            agent_filename: Filename of agent in examples/
            ticker: Ticker symbol to analyze
            mock_data: Optional mock financial data
            uploaded_file: Optional PDF file for RAG agents
            agent_class_name: Optional specific agent class name (for files with multiple agents)

        Returns:
            Dict with test results
        """
        examples_dir = Path(__file__).parent.parent / "examples"
        agent_path = examples_dir / agent_filename

        if not agent_path.exists():
            return {"success": False, "error": f"Agent file {agent_filename} not found"}

        try:
            # Dynamically load the agent module
            spec = importlib.util.spec_from_file_location("test_agent_module", agent_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["test_agent_module"] = module
            spec.loader.exec_module(module)

            # Find Agent class in module
            agent_class = self._find_agent_class(module, agent_class_name)
            if not agent_class:
                if agent_class_name:
                    return {"success": False, "error": f"Agent class '{agent_class_name}' not found in file"}
                else:
                    return {"success": False, "error": "No Agent class found in file"}

            # Create agent instance
            agent = agent_class()

            # Check if RAG agent by looking at config
            is_rag_agent = (
                hasattr(agent, 'config') and 
                agent.config and 
                hasattr(agent.config, 'rag') and 
                agent.config.rag is not None
            )

            if is_rag_agent and uploaded_file:
                # RAG agent with special analyze_async(ticker, document_text)
                return self._test_rag_agent(agent, ticker, uploaded_file)

            elif is_rag_agent:
                return {"success": False, "error": "RAG agent requires a PDF document to analyze"}

            # Traditional agent - use financial data
            # Prepare test data
            if mock_data:
                data = {"name": f"Mock Company ({ticker})", **mock_data}
            else:
                data = self._get_default_mock_data(ticker)

            # Run analysis with timing (ALL AGENTS NOW ASYNC)
            start_time = time.time()
            signal = asyncio.run(agent.analyze(ticker, data))
            execution_time = time.time() - start_time
            
            # Check if this was a fallback signal (LLM error)
            is_fallback = self._detect_llm_fallback(signal)
            llm_error_info = None
            
            if is_fallback:
                llm_error_info = self._parse_llm_error(signal.reasoning)

            # Return results
            return {
                "success": True,
                "signal": {
                    "direction": signal.direction,
                    "confidence": signal.confidence,
                    "reasoning": signal.reasoning,
                },
                "execution_time": execution_time,
                "ticker": ticker,
                "is_fallback": is_fallback,
                "llm_error_info": llm_error_info
            }

        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            # Clean up
            if "test_agent_module" in sys.modules:
                del sys.modules["test_agent_module"]

    def _test_rag_agent(self, agent, ticker: str, uploaded_file) -> Dict:
        """Test a RAG agent with PDF document.

        Args:
            agent: RAG agent instance
            ticker: Ticker symbol
            uploaded_file: Streamlit uploaded file object

        Returns:
            Test results dict
        """
        try:
            from PyPDF2 import PdfReader

            # Extract text from PDF
            pdf_reader = PdfReader(uploaded_file)
            document_text = ""
            pages_with_text = 0

            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()

                # Check if page has actual text (not scanned image)
                if page_text and len(page_text.strip()) > 50:
                    document_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                    pages_with_text += 1

            # Validate extracted text
            if not document_text.strip():
                return {
                    "success": False,
                    "error": "No text could be extracted from PDF. This PDF may be a scanned image. Try a text-based PDF with selectable text.",
                }

            if len(document_text.strip()) < 100:
                return {
                    "success": False,
                    "error": f"Only {len(document_text)} characters extracted. PDF may be scanned or corrupted. Try a different PDF.",
                }

            if pages_with_text < len(pdf_reader.pages) * 0.5:
                # Less than 50% of pages have text
                return {
                    "success": False,
                    "error": f"Only {pages_with_text}/{len(pdf_reader.pages)} pages contain text. This PDF may be partially scanned. Try a fully text-based PDF.",
                }

            # Run async analysis (RAG agents now return Signal, not dict)
            start_time = time.time()
            
            try:
                signal = asyncio.run(agent.analyze(ticker, document_text))
            except Exception as analyze_error:
                # Better error message if analyze() fails
                return {
                    "success": False,
                    "error": f"RAG analysis failed: {str(analyze_error)}. Ensure sentence-transformers is installed: pip install sentence-transformers"
                }
            
            execution_time = time.time() - start_time

            # Verify we got a Signal object
            if not hasattr(signal, 'metadata'):
                return {
                    "success": False,
                    "error": f"Agent returned {type(signal).__name__} instead of Signal object. Check agent code."
                }

            # Extract insights from signal metadata
            insights = signal.metadata.get('insights', []) if isinstance(signal.metadata, dict) else []

            # Return results
            return {
                "success": True,
                "signal": {
                    "direction": signal.direction,
                    "confidence": signal.confidence,
                    "reasoning": signal.reasoning,
                    "insights": insights,
                },
                "execution_time": execution_time,
                "ticker": ticker,
                "pages_processed": pages_with_text,
                "text_length": len(document_text),
            }

        except ImportError:
            return {
                "success": False,
                "error": "PyPDF2 not installed. Install with: pip install pypdf2",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"PDF analysis error: {str(e)}. Check that the PDF contains selectable text (not a scanned image).",
            }

    def _find_agent_class(self, module, agent_class_name: Optional[str] = None):
        """Find the Agent class in a module.
        
        Args:
            module: Python module
            agent_class_name: Optional specific class name to find

        Returns:
            Agent class or None
        """
        from agent_framework import Agent
        
        # If specific class name requested, find that one
        if agent_class_name:
            for name in dir(module):
                if name == agent_class_name:
                    obj = getattr(module, name)
                    # Verify it's an Agent subclass
                    if isinstance(obj, type) and issubclass(obj, Agent) and obj is not Agent:
                        return obj
            return None

        # Otherwise, find first Agent subclass
        for name in dir(module):
            obj = getattr(module, name)

            # Check if it's a class that inherits from Agent
            if isinstance(obj, type) and issubclass(obj, Agent) and obj is not Agent:
                return obj

        return None

    def _get_default_mock_data(self, ticker: str) -> Dict:
        """Get default mock data for testing.

        Args:
            ticker: Ticker symbol

        Returns:
            Mock financial data
        """
        # Provide reasonable defaults
        return {
            "name": f"Test Company ({ticker})",
            "pe_ratio": 20.0,
            "pb_ratio": 3.5,
            "roe": 15.0,
            "profit_margin": 12.0,
            "revenue_growth": 15.0,
            "debt_to_equity": 0.8,
            "current_ratio": 1.5,
            "dividend_yield": 2.0,
            "market_cap": 500_000_000_000,  # $500B
        }
    
    def _detect_llm_fallback(self, signal) -> bool:
        """Detect if signal is from LLM fallback (error occurred).
        
        Args:
            signal: Signal object
            
        Returns:
            True if this is a fallback signal
        """
        reasoning = signal.reasoning.lower()
        
        # Check for fallback indicators
        fallback_indicators = [
            'llm unavailable',
            'llm error',
            'using fallback',
            'no module named',
            'connection refused',
            'api error',
            'rate limit',
            'authentication',
            'api key'
        ]
        
        return any(indicator in reasoning for indicator in fallback_indicators)
    
    def _parse_llm_error(self, reasoning: str) -> Dict:
        """Parse LLM error reasoning to extract useful information.
        
        Args:
            reasoning: Signal reasoning string
            
        Returns:
            Dict with error type and installation instructions
        """
        reasoning_lower = reasoning.lower()
        
        # Detect specific error types
        error_info = {
            "error_type": "unknown",
            "provider": None,
            "model": None,
            "install_command": None,
            "description": ""
        }
        
        # Module not found errors
        if "no module named 'ollama'" in reasoning_lower:
            error_info.update({
                "error_type": "missing_package",
                "provider": "ollama",
                "install_command": "pip install ollama",
                "description": "Ollama Python package not installed"
            })
        elif "no module named 'openai'" in reasoning_lower:
            error_info.update({
                "error_type": "missing_package",
                "provider": "openai",
                "install_command": "pip install openai",
                "description": "OpenAI Python package not installed"
            })
        elif "no module named 'anthropic'" in reasoning_lower:
            error_info.update({
                "error_type": "missing_package",
                "provider": "anthropic",
                "install_command": "pip install anthropic",
                "description": "Anthropic Python package not installed"
            })
        
        # Connection errors (Ollama not running)
        elif "connection refused" in reasoning_lower or "connect" in reasoning_lower:
            error_info.update({
                "error_type": "connection_error",
                "provider": "ollama",
                "install_command": None,
                "description": "Ollama service not running. Start with: ollama serve"
            })
        
        # Model not found (need to pull)
        elif "model" in reasoning_lower and "not found" in reasoning_lower:
            # Try to extract model name from reasoning
            import re
            model_match = re.search(r"model[\s'\"]*([a-z0-9\.:_-]+)", reasoning_lower)
            model_name = model_match.group(1) if model_match else "llama3.2"
            
            error_info.update({
                "error_type": "model_not_found",
                "provider": "ollama",
                "model": model_name,
                "install_command": f"ollama pull {model_name}",
                "description": f"Model '{model_name}' not downloaded in Ollama"
            })
        
        # API key errors
        elif "api key" in reasoning_lower or "authentication" in reasoning_lower:
            if "openai" in reasoning_lower:
                provider = "openai"
                env_var = "OPENAI_API_KEY"
            elif "anthropic" in reasoning_lower:
                provider = "anthropic"
                env_var = "ANTHROPIC_API_KEY"
            else:
                provider = "unknown"
                env_var = "API_KEY"
            
            error_info.update({
                "error_type": "missing_api_key",
                "provider": provider,
                "install_command": None,
                "description": f"API key not configured. Set {env_var} in .env file"
            })
        
        # Rate limit errors
        elif "rate limit" in reasoning_lower:
            error_info.update({
                "error_type": "rate_limit",
                "provider": None,
                "install_command": None,
                "description": "API rate limit exceeded. Wait a few minutes and try again."
            })
        
        # Generic LLM error
        else:
            error_info.update({
                "error_type": "llm_error",
                "provider": None,
                "install_command": None,
                "description": "LLM service encountered an error"
            })
        
        return error_info
