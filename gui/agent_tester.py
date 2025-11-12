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
        uploaded_file: Optional[Any] = None
    ) -> Dict:
        """Test an agent with provided data.
        
        Args:
            agent_filename: Filename of agent in examples/
            ticker: Ticker symbol to analyze
            mock_data: Optional mock financial data
            uploaded_file: Optional PDF file for RAG agents
            
        Returns:
            Dict with test results
        """
        examples_dir = Path(__file__).parent.parent / "examples"
        agent_path = examples_dir / agent_filename
        
        if not agent_path.exists():
            return {
                'success': False,
                'error': f'Agent file {agent_filename} not found'
            }
        
        try:
            # Dynamically load the agent module
            spec = importlib.util.spec_from_file_location(
                "test_agent_module",
                agent_path
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules['test_agent_module'] = module
            spec.loader.exec_module(module)
            
            # Find Agent class in module
            agent_class = self._find_agent_class(module)
            if not agent_class:
                return {
                    'success': False,
                    'error': 'No Agent class found in file'
                }
            
            # Create agent instance
            agent = agent_class()
            
            # Check if RAG agent (has analyze_async method)
            is_rag_agent = hasattr(agent, 'analyze_async') and callable(getattr(agent, 'analyze_async'))
            
            if is_rag_agent and uploaded_file:
                # RAG agent - extract PDF text and analyze
                return self._test_rag_agent(agent, ticker, uploaded_file)
            
            elif is_rag_agent:
                return {
                    'success': False,
                    'error': 'RAG agent requires a PDF document to analyze'
                }
            
            # Traditional agent - use financial data
            # Prepare test data
            if mock_data:
                data = {
                    'name': f'Mock Company ({ticker})',
                    **mock_data
                }
            else:
                data = self._get_default_mock_data(ticker)
            
            # Run analysis with timing
            start_time = time.time()
            signal = agent.analyze(ticker, data)
            execution_time = time.time() - start_time
            
            # Return results
            return {
                'success': True,
                'signal': {
                    'direction': signal.direction,
                    'confidence': signal.confidence,
                    'reasoning': signal.reasoning
                },
                'execution_time': execution_time,
                'ticker': ticker
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            # Clean up
            if 'test_agent_module' in sys.modules:
                del sys.modules['test_agent_module']
    
    def _test_rag_agent(
        self,
        agent,
        ticker: str,
        uploaded_file
    ) -> Dict:
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
                    'success': False,
                    'error': 'No text could be extracted from PDF. This PDF may be a scanned image. Try a text-based PDF with selectable text.'
                }
            
            if len(document_text.strip()) < 100:
                return {
                    'success': False,
                    'error': f'Only {len(document_text)} characters extracted. PDF may be scanned or corrupted. Try a different PDF.'
                }
            
            if pages_with_text < len(pdf_reader.pages) * 0.5:
                # Less than 50% of pages have text
                return {
                    'success': False,
                    'error': f'Only {pages_with_text}/{len(pdf_reader.pages)} pages contain text. This PDF may be partially scanned. Try a fully text-based PDF.'
                }
            
            # Run async analysis
            start_time = time.time()
            result_dict = asyncio.run(agent.analyze_async(ticker, document_text))
            execution_time = time.time() - start_time
            
            # Return RAG results (dict format, not Signal)
            return {
                'success': True,
                'signal': {
                    'direction': result_dict.get('direction', 'neutral'),
                    'confidence': result_dict.get('confidence', 0.5),
                    'reasoning': result_dict.get('reasoning', 'No reasoning provided'),
                    'insights': result_dict.get('insights', [])
                },
                'execution_time': execution_time,
                'ticker': ticker,
                'pages_processed': pages_with_text,
                'text_length': len(document_text)
            }
            
        except ImportError:
            return {
                'success': False,
                'error': 'PyPDF2 not installed. Install with: pip install pypdf2'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'PDF analysis error: {str(e)}. Check that the PDF contains selectable text (not a scanned image).'
            }
    
    def _find_agent_class(self, module):
        """Find the Agent class in a module.
        
        Args:
            module: Python module
            
        Returns:
            Agent class or None
        """
        from agent_framework import Agent
        
        for name in dir(module):
            obj = getattr(module, name)
            
            # Check if it's a class that inherits from Agent
            if (isinstance(obj, type) and 
                issubclass(obj, Agent) and 
                obj is not Agent):
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
            'name': f'Test Company ({ticker})',
            'pe_ratio': 20.0,
            'pb_ratio': 3.5,
            'roe': 15.0,
            'profit_margin': 12.0,
            'revenue_growth': 15.0,
            'debt_to_equity': 0.8,
            'current_ratio': 1.5,
            'dividend_yield': 2.0,
            'market_cap': 500_000_000_000  # $500B
        }
