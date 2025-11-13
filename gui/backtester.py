"""Basic Backtesting Module for Educational Purposes

Provides simple historical performance testing of agents.
Shows win rate, signal distribution, and basic metrics.

⚠️ DISCLAIMER: This is for educational purposes only.
Backtested results do NOT guarantee future performance.
See DISCLAIMER.md for full terms.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import importlib.util

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_framework import Database, Config


class BacktestResult:
    """Results from a backtest run."""
    
    def __init__(self):
        self.total_signals = 0
        self.bullish_count = 0
        self.bearish_count = 0
        self.neutral_count = 0
        self.signals_by_ticker = {}
        self.avg_confidence = 0.0
        self.execution_time = 0.0
        
    def add_signal(self, ticker: str, signal):
        """Add a signal to results."""
        self.total_signals += 1
        
        if signal.direction == 'bullish':
            self.bullish_count += 1
        elif signal.direction == 'bearish':
            self.bearish_count += 1
        else:
            self.neutral_count += 1
        
        if ticker not in self.signals_by_ticker:
            self.signals_by_ticker[ticker] = []
        
        self.signals_by_ticker[ticker].append({
            'direction': signal.direction,
            'confidence': signal.confidence,
            'reasoning': signal.reasoning
        })
    
    def calculate_stats(self):
        """Calculate aggregate statistics."""
        if self.total_signals > 0:
            total_conf = 0
            for ticker_signals in self.signals_by_ticker.values():
                for sig in ticker_signals:
                    total_conf += sig['confidence']
            self.avg_confidence = total_conf / self.total_signals
    
    def get_win_rate(self) -> float:
        """Calculate win rate (bullish signals / total actionable signals).
        
        Note: This is a simplified metric for educational purposes.
        Real win rate requires comparing signals to actual price movements.
        """
        actionable = self.bullish_count + self.bearish_count
        if actionable == 0:
            return 0.0
        return self.bullish_count / actionable
    
    def to_dict(self) -> Dict:
        """Convert results to dictionary."""
        return {
            'total_signals': self.total_signals,
            'bullish_count': self.bullish_count,
            'bearish_count': self.bearish_count,
            'neutral_count': self.neutral_count,
            'avg_confidence': self.avg_confidence,
            'win_rate': self.get_win_rate(),
            'signals_by_ticker': self.signals_by_ticker,
            'execution_time': self.execution_time
        }


class Backtester:
    """Simple backtesting engine for educational purposes.
    
    This provides basic historical testing to help students understand
    how their rules would have performed on sample data.
    
    Limitations:
    - Uses static sample data (not real historical prices)
    - No execution simulation (assumes perfect fills)
    - No transaction costs or slippage
    - Simplified win rate calculation
    
    For production backtesting, use specialized tools like:
    - Backtrader, Zipline, QuantConnect
    """
    
    async def run_backtest(
        self,
        agent_filename: str,
        tickers: List[str],
        use_database: bool = True,
        agent_class_name: Optional[str] = None,
    ) -> Tuple[bool, BacktestResult, Optional[str]]:
        """Run basic backtest on historical data.
        
        Args:
            agent_filename: Path to agent file
            tickers: List of tickers to test
            use_database: Whether to use database (False = mock data)
            agent_class_name: Optional specific agent class name (for files with multiple agents)
            
        Returns:
            Tuple of (success, BacktestResult, error_message)
        """
        result = BacktestResult()
        start_time = datetime.now()
        
        try:
            # Load agent
            agent = self._load_agent(agent_filename, agent_class_name)
            if not agent:
                if agent_class_name:
                    return False, result, f"Agent class '{agent_class_name}' not found in {agent_filename}"
                else:
                    return False, result, "Failed to load agent"
            
            # Get data
            if use_database:
                data_points = await self._get_database_data(tickers)
            else:
                data_points = self._get_mock_data(tickers)
            
            # Run agent on each data point
            for ticker, data in data_points:
                try:
                    signal = agent.analyze(ticker, data)
                    result.add_signal(ticker, signal)
                except Exception as e:
                    return False, result, f"Agent error on {ticker}: {str(e)}"
            
            # Calculate statistics
            result.calculate_stats()
            result.execution_time = (datetime.now() - start_time).total_seconds()
            
            return True, result, None
            
        except Exception as e:
            return False, result, f"Backtest error: {str(e)}"
    
    def _load_agent(self, agent_filename: str, agent_class_name: Optional[str] = None):
        """Load agent from file.
        
        Args:
            agent_filename: Agent filename
            agent_class_name: Optional specific class name (for multi-agent files)
            
        Returns:
            Agent instance or None
        """
        try:
            examples_dir = Path(__file__).parent.parent / "examples"
            agent_path = examples_dir / agent_filename
            
            if not agent_path.exists():
                return None
            
            # Import agent module
            spec = importlib.util.spec_from_file_location("agent_module", agent_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Import Agent base class
            from agent_framework import Agent
            
            # If specific class name requested, find that one
            if agent_class_name:
                for item_name in dir(module):
                    if item_name == agent_class_name:
                        item = getattr(module, item_name)
                        # Verify it's an Agent subclass
                        if isinstance(item, type) and issubclass(item, Agent) and item is not Agent:
                            return item()
                # Class not found
                print(f"Agent class '{agent_class_name}' not found in {agent_filename}")
                return None
            
            # Otherwise, find first Agent subclass (backward compatibility)
            for item_name in dir(module):
                item = getattr(module, item_name)
                if (isinstance(item, type) and 
                    issubclass(item, Agent) and 
                    item is not Agent):
                    return item()
            
            return None
            
        except Exception as e:
            print(f"Error loading agent: {e}")
            return None
    
    async def _get_database_data(self, tickers: List[str]) -> List[Tuple[str, Dict]]:
        """Get data from database.
        
        Returns list of (ticker, data) tuples.
        """
        data_points = []
        
        db = Database(Config.get_database_url())
        await db.connect()
        
        try:
            for ticker in tickers:
                fundamentals = await db.get_fundamentals(ticker)
                if fundamentals:
                    data_points.append((ticker, fundamentals))
        finally:
            await db.disconnect()
        
        return data_points
    
    def _get_mock_data(self, tickers: List[str]) -> List[Tuple[str, Dict]]:
        """Generate mock data for testing without database.
        
        Returns list of (ticker, data) tuples.
        """
        # Mock data variations for backtesting
        mock_scenarios = [
            # Undervalued scenarios
            {
                'pe_ratio': 12.0,
                'revenue_growth': 8.0,
                'profit_margin': 18.0,
                'roe': 16.0,
                'debt_to_equity': 0.4,
                'dividend_yield': 2.5,
                'pb_ratio': 2.0,
                'current_ratio': 1.8
            },
            # Growth scenarios
            {
                'pe_ratio': 35.0,
                'revenue_growth': 28.0,
                'profit_margin': 22.0,
                'roe': 25.0,
                'debt_to_equity': 0.3,
                'dividend_yield': 0.5,
                'pb_ratio': 8.0,
                'current_ratio': 2.0
            },
            # Overvalued scenarios
            {
                'pe_ratio': 45.0,
                'revenue_growth': 5.0,
                'profit_margin': 12.0,
                'roe': 11.0,
                'debt_to_equity': 1.8,
                'dividend_yield': 1.0,
                'pb_ratio': 4.0,
                'current_ratio': 1.2
            },
            # Balanced scenarios
            {
                'pe_ratio': 20.0,
                'revenue_growth': 15.0,
                'profit_margin': 16.0,
                'roe': 18.0,
                'debt_to_equity': 0.6,
                'dividend_yield': 2.0,
                'pb_ratio': 3.5,
                'current_ratio': 1.5
            },
            # High debt scenarios
            {
                'pe_ratio': 18.0,
                'revenue_growth': 10.0,
                'profit_margin': 14.0,
                'roe': 15.0,
                'debt_to_equity': 2.5,
                'dividend_yield': 1.5,
                'pb_ratio': 2.5,
                'current_ratio': 1.1
            }
        ]
        
        data_points = []
        
        for i, ticker in enumerate(tickers):
            # Cycle through scenarios
            scenario = mock_scenarios[i % len(mock_scenarios)]
            data_points.append((ticker, scenario))
        
        return data_points


# For testing
if __name__ == "__main__":
    import asyncio
    
    async def test():
        """Test backtesting functionality."""
        backtester = Backtester()
        
        # Test with mock data
        success, result, error = await backtester.run_backtest(
            "01_basic.py",
            ["AAPL", "MSFT", "TSLA", "JPM", "GOOGL"],
            use_database=False
        )
        
        if success:
            print("Backtest Results:")
            print(f"Total Signals: {result.total_signals}")
            print(f"Bullish: {result.bullish_count}")
            print(f"Bearish: {result.bearish_count}")
            print(f"Neutral: {result.neutral_count}")
            print(f"Avg Confidence: {result.avg_confidence:.1%}")
            print(f"Win Rate: {result.get_win_rate():.1%}")
        else:
            print(f"Error: {error}")
    
    asyncio.run(test())
