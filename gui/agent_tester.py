"""Agent Tester - Test agents with mock or real data"""

import sys
import importlib.util
import time
from pathlib import Path
from typing import Dict, Optional


class AgentTester:
    """Test agents with mock or database data."""
    
    def test_agent(
        self,
        agent_filename: str,
        ticker: str,
        mock_data: Optional[Dict] = None
    ) -> Dict:
        """Test an agent with provided data.
        
        Args:
            agent_filename: Filename of agent in examples/
            ticker: Ticker symbol to analyze
            mock_data: Optional mock financial data
            
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
