"""
Mock Data Generator
Generates comprehensive test data for all agent types:
- Fundamental, Macro, Technical, Sentiment, Risk
"""

import random
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class MockDataGenerator:
    """
    Comprehensive mock data generator for all agent types

    Usage:
        generator = MockDataGenerator()
        generator.generate_all_data(tickers=['AAPL', 'MSFT'], days=90)
        generator.insert_to_database(db_connection)
    """

    # Enhanced ticker profiles
    TICKER_PROFILES = {
        "AAPL": {
            "name": "Apple Inc.",
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "price_range": (150, 200),
            "volatility": 0.02,
            "trend": "bullish",
            "pe_ratio": 28.5,
            "market_cap": 2800000000000,
            "revenue": 390000000000,
            "growth_rate": 0.08,
            "quality": "high",
        },
        "MSFT": {
            "name": "Microsoft Corporation",
            "sector": "Technology",
            "industry": "Software",
            "price_range": (350, 420),
            "volatility": 0.015,
            "trend": "bullish",
            "pe_ratio": 32.1,
            "market_cap": 2600000000000,
            "revenue": 220000000000,
            "growth_rate": 0.12,
            "quality": "high",
        },
        "GOOGL": {
            "name": "Alphabet Inc.",
            "sector": "Technology",
            "industry": "Internet Services",
            "price_range": (130, 160),
            "volatility": 0.018,
            "trend": "neutral",
            "pe_ratio": 24.3,
            "market_cap": 1700000000000,
            "revenue": 280000000000,
            "growth_rate": 0.10,
            "quality": "high",
        },
        "TSLA": {
            "name": "Tesla Inc.",
            "sector": "Automotive",
            "industry": "Electric Vehicles",
            "price_range": (200, 280),
            "volatility": 0.035,
            "trend": "volatile",
            "pe_ratio": 65.2,
            "market_cap": 850000000000,
            "revenue": 95000000000,
            "growth_rate": 0.25,
            "quality": "medium",
        },
        "AMZN": {
            "name": "Amazon.com Inc.",
            "sector": "E-commerce",
            "industry": "Internet Retail",
            "price_range": (140, 180),
            "volatility": 0.02,
            "trend": "bullish",
            "pe_ratio": 45.8,
            "market_cap": 1500000000000,
            "revenue": 520000000000,
            "growth_rate": 0.11,
            "quality": "high",
        },
        "JPM": {
            "name": "JPMorgan Chase & Co.",
            "sector": "Banking",
            "industry": "Financial Services",
            "price_range": (145, 170),
            "volatility": 0.015,
            "trend": "neutral",
            "pe_ratio": 11.2,
            "market_cap": 450000000000,
            "revenue": 130000000000,
            "growth_rate": 0.05,
            "quality": "high",
        },
        "XOM": {
            "name": "Exxon Mobil Corporation",
            "sector": "Energy",
            "industry": "Oil & Gas",
            "price_range": (100, 120),
            "volatility": 0.025,
            "trend": "bearish",
            "pe_ratio": 8.5,
            "market_cap": 420000000000,
            "revenue": 380000000000,
            "growth_rate": 0.03,
            "quality": "medium",
        },
        "WMT": {
            "name": "Walmart Inc.",
            "sector": "Retail",
            "industry": "Discount Stores",
            "price_range": (50, 65),
            "volatility": 0.012,
            "trend": "neutral",
            "pe_ratio": 26.3,
            "market_cap": 380000000000,
            "revenue": 610000000000,
            "growth_rate": 0.04,
            "quality": "high",
        },
    }

    def __init__(self):
        self.data = {
            "fundamentals": [],
            "prices": [],
            "news": [],
            "analyst_ratings": [],
            "insider_trades": [],
            "balance_sheet": [],
            "cash_flow": [],
            "earnings": [],
            "sec_filings": [],
            "technical_indicators": [],
            "risk_metrics": [],
            "options_data": [],
            "macro_indicators": [],
        }

    def generate_all_data(self, tickers: List[str] = None, days: int = 90):
        """Generate all mock data"""
        if tickers is None:
            tickers = list(self.TICKER_PROFILES.keys())

        logger.info(f"Generating mock data for {len(tickers)} tickers, {days} days...")

        # Generate macro data first (shared across all tickers)
        self.data["macro_indicators"] = self._generate_macro_data(days)
        logger.info(
            f"  ✅ Generated {len(self.data['macro_indicators'])} macro indicators"
        )

        for ticker in tickers:
            if ticker not in self.TICKER_PROFILES:
                logger.warning(f"Unknown ticker {ticker}, skipping")
                continue

            profile = self.TICKER_PROFILES[ticker]
            logger.info(f"  Generating data for {ticker}...")

            # Core data
            self.data["fundamentals"].append(
                self._generate_fundamentals(ticker, profile)
            )
            prices = self._generate_prices(ticker, profile, days)
            self.data["prices"].extend(prices)

            # Technical indicators (based on prices)
            self.data["technical_indicators"].extend(
                self._generate_technical_indicators(ticker, prices)
            )

            # Risk metrics (based on prices)
            self.data["risk_metrics"].extend(
                self._generate_risk_metrics(ticker, prices)
            )

            # Options data
            self.data["options_data"].extend(
                self._generate_options_data(ticker, profile, days)
            )

            # Fundamental details
            self.data["balance_sheet"].extend(
                self._generate_balance_sheet(ticker, profile)
            )
            self.data["cash_flow"].extend(self._generate_cash_flow(ticker, profile))
            self.data["earnings"].extend(self._generate_earnings(ticker, profile))

            # SEC filings
            self.data["sec_filings"].extend(self._generate_sec_filings(ticker, profile))

            # Sentiment data
            self.data["news"].extend(self._generate_news(ticker, profile, days))
            self.data["analyst_ratings"].extend(
                self._generate_analyst_ratings(ticker, profile)
            )
            self.data["insider_trades"].extend(
                self._generate_insider_trades(ticker, profile)
            )

        logger.info(
            f"""
✅ Generated complete dataset:
   - Fundamentals: {len(self.data['fundamentals'])}
   - Prices: {len(self.data['prices'])}
   - Technical Indicators: {len(self.data['technical_indicators'])}
   - Risk Metrics: {len(self.data['risk_metrics'])}
   - Balance Sheets: {len(self.data['balance_sheet'])}
   - Cash Flow: {len(self.data['cash_flow'])}
   - Earnings: {len(self.data['earnings'])}
   - SEC Filings: {len(self.data['sec_filings'])}
   - News: {len(self.data['news'])}
   - Analyst Ratings: {len(self.data['analyst_ratings'])}
   - Insider Trades: {len(self.data['insider_trades'])}
   - Options Data: {len(self.data['options_data'])}
   - Macro Indicators: {len(self.data['macro_indicators'])}
        """
        )

        return self.data

    def _generate_fundamentals(self, ticker: str, profile: Dict) -> Dict:
        """Generate enhanced fundamental metrics"""
        pe_ratio = profile["pe_ratio"]
        market_cap = profile["market_cap"]
        revenue = profile["revenue"]

        # Derive metrics
        earnings = market_cap / pe_ratio
        eps = earnings / (market_cap / 150)  # Assume shares outstanding

        net_income = revenue * random.uniform(0.08, 0.25)

        return {
            "ticker": ticker,
            "company_name": profile["name"],
            "sector": profile["sector"],
            "industry": profile["industry"],
            # Valuation
            "market_cap": market_cap,
            "enterprise_value": int(market_cap * random.uniform(1.05, 1.15)),
            "pe_ratio": pe_ratio,
            "forward_pe": round(pe_ratio * random.uniform(0.9, 1.0), 2),
            "peg_ratio": round(pe_ratio / (profile["growth_rate"] * 100), 2),
            "pb_ratio": round(random.uniform(2, 8), 2),
            "ps_ratio": round(market_cap / revenue, 2),
            "pcf_ratio": round(random.uniform(8, 20), 2),
            "dividend_yield": round(random.uniform(0, 3), 2),
            # Profitability
            "earnings_per_share": round(eps, 2),
            "revenue": int(revenue),
            "revenue_growth": round(profile["growth_rate"] * 100, 2),
            "net_income": int(net_income),
            "profit_margin": round((net_income / revenue) * 100, 2),
            "operating_margin": round(random.uniform(15, 35), 2),
            "gross_margin": round(random.uniform(30, 60), 2),
            "roe": round(random.uniform(10, 30), 2),
            "roa": round(random.uniform(5, 15), 2),
            "roic": round(random.uniform(8, 20), 2),
            # Financial health
            "debt_to_equity": round(random.uniform(0.2, 1.5), 2),
            "current_ratio": round(random.uniform(1.0, 2.5), 2),
            "quick_ratio": round(random.uniform(0.8, 2.0), 2),
            "cash_ratio": round(random.uniform(0.3, 1.2), 2),
            "interest_coverage": round(random.uniform(5, 20), 2),
            # Efficiency
            "asset_turnover": round(random.uniform(0.5, 2.0), 2),
            "inventory_turnover": round(random.uniform(4, 12), 2),
            # Growth
            "earnings_growth": round(
                profile["growth_rate"] * 100 * random.uniform(0.9, 1.1), 2
            ),
            "book_value_per_share": round(random.uniform(20, 100), 2),
            # Risk
            "beta": round(random.uniform(0.8, 1.5), 2),
            "updated_at": datetime.now(),
        }

    def _generate_prices(self, ticker: str, profile: Dict, days: int) -> List[Dict]:
        """Generate price data with realistic trends"""
        prices = []
        min_price, max_price = profile["price_range"]
        volatility = profile["volatility"]
        trend = profile["trend"]

        current_price = random.uniform(min_price, max_price)

        trend_multipliers = {
            "bullish": 1.0002,
            "bearish": 0.9998,
            "neutral": 1.0000,
            "volatile": 1.0000,
        }
        trend_mult = trend_multipliers[trend]

        start_date = datetime.now() - timedelta(days=days)

        for i in range(days):
            date = start_date + timedelta(days=i)

            # Skip weekends
            if date.weekday() >= 5:
                continue

            # Apply trend and volatility
            change = random.gauss(0, volatility)
            current_price *= (1 + change) * trend_mult

            # Keep within reasonable bounds
            current_price = max(min_price * 0.8, min(max_price * 1.2, current_price))

            # Generate OHLC
            open_price = current_price * random.uniform(0.995, 1.005)
            high_price = max(open_price, current_price) * random.uniform(1.000, 1.015)
            low_price = min(open_price, current_price) * random.uniform(0.985, 1.000)
            close_price = current_price

            # Generate volume (higher on volatile days)
            base_volume = random.uniform(50000000, 150000000)
            volume_multiplier = 1 + abs(change) * 10
            volume = int(base_volume * volume_multiplier)

            # VWAP calculation
            vwap = (high_price + low_price + close_price) / 3

            prices.append(
                {
                    "ticker": ticker,
                    "date": date.date(),
                    "open": round(open_price, 2),
                    "high": round(high_price, 2),
                    "low": round(low_price, 2),
                    "close": round(close_price, 2),
                    "volume": volume,
                    "vwap": round(vwap, 2),
                }
            )

        return prices

    def _generate_technical_indicators(
        self, ticker: str, prices: List[Dict]
    ) -> List[Dict]:
        """Generate technical indicators from price data"""
        indicators = []

        # Sort prices by date
        sorted_prices = sorted(prices, key=lambda x: x["date"])

        for i, price_data in enumerate(sorted_prices):
            if i < 20:  # Need minimum data for indicators
                continue

            recent_prices = [p["close"] for p in sorted_prices[max(0, i - 200) : i + 1]]
            recent_volumes = [
                p["volume"] for p in sorted_prices[max(0, i - 200) : i + 1]
            ]

            # Calculate indicators
            sma_20 = sum(recent_prices[-20:]) / 20 if len(recent_prices) >= 20 else None
            sma_50 = sum(recent_prices[-50:]) / 50 if len(recent_prices) >= 50 else None
            sma_200 = (
                sum(recent_prices[-200:]) / 200 if len(recent_prices) >= 200 else None
            )

            # EMA calculation (simplified)
            ema_12 = recent_prices[-1] * 0.154 + (sma_20 * 0.846) if sma_20 else None
            ema_26 = recent_prices[-1] * 0.074 + (sma_20 * 0.926) if sma_20 else None

            # Simple RSI calculation
            changes = [
                recent_prices[j] - recent_prices[j - 1]
                for j in range(1, min(15, len(recent_prices)))
            ]
            gains = [c for c in changes if c > 0]
            losses = [-c for c in changes if c < 0]
            avg_gain = sum(gains) / len(gains) if gains else 0.1
            avg_loss = sum(losses) / len(losses) if losses else 0.1
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            # MACD (simplified)
            if ema_12 and ema_26:
                macd = ema_12 - ema_26
                macd_signal = macd * 0.8
                macd_histogram = macd - macd_signal
            else:
                macd = macd_signal = macd_histogram = 0

            # Bollinger Bands
            if sma_20:
                std_dev = (
                    sum((p - sma_20) ** 2 for p in recent_prices[-20:]) / 20
                ) ** 0.5
                bollinger_upper = sma_20 + 2 * std_dev
                bollinger_lower = sma_20 - 2 * std_dev
            else:
                bollinger_upper = bollinger_lower = None

            # ATR (simplified)
            if i >= 14:
                true_ranges = []
                for j in range(i - 14, i):
                    high = sorted_prices[j]["high"]
                    low = sorted_prices[j]["low"]
                    prev_close = sorted_prices[j - 1]["close"] if j > 0 else low
                    tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
                    true_ranges.append(tr)
                atr_14 = sum(true_ranges) / len(true_ranges)
            else:
                atr_14 = 0

            indicators.append(
                {
                    "ticker": ticker,
                    "date": price_data["date"],
                    "sma_20": round(sma_20, 2) if sma_20 else None,
                    "sma_50": round(sma_50, 2) if sma_50 else None,
                    "sma_200": round(sma_200, 2) if sma_200 else None,
                    "ema_12": round(ema_12, 2) if ema_12 else None,
                    "ema_26": round(ema_26, 2) if ema_26 else None,
                    "rsi_14": round(rsi, 2),
                    "macd": round(macd, 4),
                    "macd_signal": round(macd_signal, 4),
                    "macd_histogram": round(macd_histogram, 4),
                    "bollinger_upper": (
                        round(bollinger_upper, 2) if bollinger_upper else None
                    ),
                    "bollinger_middle": round(sma_20, 2) if sma_20 else None,
                    "bollinger_lower": (
                        round(bollinger_lower, 2) if bollinger_lower else None
                    ),
                    "atr_14": round(atr_14, 2),
                    "obv": sum(recent_volumes),
                    "adx_14": round(random.uniform(15, 45), 2),
                }
            )

        return indicators

    def _generate_risk_metrics(self, ticker: str, prices: List[Dict]) -> List[Dict]:
        """Generate risk metrics from price data"""
        metrics = []
        sorted_prices = sorted(prices, key=lambda x: x["date"])

        for i, price_data in enumerate(sorted_prices):
            if i < 30:  # Need minimum data
                continue

            recent_prices = [p["close"] for p in sorted_prices[max(0, i - 90) : i + 1]]

            # Calculate returns
            returns = [
                (recent_prices[j] - recent_prices[j - 1]) / recent_prices[j - 1] * 100
                for j in range(1, len(recent_prices))
            ]

            if len(returns) < 10:
                continue

            # Volatility (annualized)
            mean_return = sum(returns) / len(returns)
            variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
            daily_vol = variance**0.5
            vol_30d = daily_vol * (252**0.5)  # Annualized

            returns_90d = returns if len(returns) <= 90 else returns[-90:]
            mean_90 = sum(returns_90d) / len(returns_90d)
            var_90 = sum((r - mean_90) ** 2 for r in returns_90d) / len(returns_90d)
            vol_90d = (var_90**0.5) * (252**0.5)

            # VaR (simplified)
            sorted_returns = sorted(returns)
            var_95 = (
                sorted_returns[int(len(sorted_returns) * 0.05)]
                if len(sorted_returns) > 20
                else -5
            )
            var_99 = (
                sorted_returns[int(len(sorted_returns) * 0.01)]
                if len(sorted_returns) > 100
                else -8
            )

            # Max drawdown
            peak = max(recent_prices)
            peak_idx = recent_prices.index(peak)
            trough = (
                min(recent_prices[peak_idx:])
                if peak_idx < len(recent_prices)
                else recent_prices[-1]
            )
            max_dd = ((trough - peak) / peak) * 100

            # Returns
            return_1d = returns[-1] if returns else 0
            return_1w = sum(returns[-5:]) if len(returns) >= 5 else 0
            return_1m = sum(returns[-20:]) if len(returns) >= 20 else 0
            return_3m = sum(returns[-60:]) if len(returns) >= 60 else 0
            return_ytd = sum(returns)

            # Sharpe ratio (assuming risk-free rate of 4% annual)
            risk_free_daily = 4 / 252
            excess_returns = [r - risk_free_daily for r in returns]
            avg_excess = sum(excess_returns) / len(excess_returns)
            sharpe = (avg_excess / daily_vol) * (252**0.5) if daily_vol > 0 else 0

            # Sortino (only downside deviation)
            downside_returns = [r for r in excess_returns if r < 0]
            if downside_returns:
                downside_dev = (
                    sum(r**2 for r in downside_returns) / len(downside_returns)
                ) ** 0.5
                sortino = (
                    (avg_excess / downside_dev) * (252**0.5) if downside_dev > 0 else 0
                )
            else:
                sortino = sharpe * 1.2

            metrics.append(
                {
                    "ticker": ticker,
                    "date": price_data["date"],
                    "historical_volatility_30d": round(vol_30d, 2),
                    "historical_volatility_90d": round(vol_90d, 2),
                    "implied_volatility": round(vol_30d * random.uniform(1.1, 1.3), 2),
                    "value_at_risk_95": round(var_95, 2),
                    "value_at_risk_99": round(var_99, 2),
                    "max_drawdown": round(max_dd, 2),
                    "return_1d": round(return_1d, 2),
                    "return_1w": round(return_1w, 2),
                    "return_1m": round(return_1m, 2),
                    "return_3m": round(return_3m, 2),
                    "return_ytd": round(return_ytd, 2),
                    "sharpe_ratio": round(sharpe, 2),
                    "sortino_ratio": round(sortino, 2),
                    "correlation_sp500": round(random.uniform(0.3, 0.9), 3),
                }
            )

        return metrics

    def _generate_balance_sheet(self, ticker: str, profile: Dict) -> List[Dict]:
        """Generate quarterly balance sheet data"""
        sheets = []
        revenue = profile["revenue"]

        for i in range(4):  # Last 4 quarters
            quarter = f"2024-Q{4-i}"

            total_assets = int(revenue * random.uniform(1.2, 2.0))
            current_assets = int(total_assets * random.uniform(0.3, 0.5))
            total_liabilities = int(total_assets * random.uniform(0.4, 0.7))
            current_liabilities = int(total_liabilities * random.uniform(0.4, 0.6))

            sheets.append(
                {
                    "ticker": ticker,
                    "quarter": quarter,
                    "total_assets": total_assets,
                    "current_assets": current_assets,
                    "cash_and_equivalents": int(
                        current_assets * random.uniform(0.3, 0.6)
                    ),
                    "accounts_receivable": int(
                        current_assets * random.uniform(0.2, 0.4)
                    ),
                    "inventory": int(current_assets * random.uniform(0.1, 0.3)),
                    "total_liabilities": total_liabilities,
                    "current_liabilities": current_liabilities,
                    "long_term_debt": int(total_liabilities * random.uniform(0.3, 0.5)),
                    "short_term_debt": int(
                        current_liabilities * random.uniform(0.2, 0.4)
                    ),
                    "shareholders_equity": total_assets - total_liabilities,
                    "retained_earnings": int(
                        (total_assets - total_liabilities) * random.uniform(0.5, 0.8)
                    ),
                    "filing_date": (datetime.now() - timedelta(days=90 * i)).date(),
                }
            )

        return sheets

    def _generate_cash_flow(self, ticker: str, profile: Dict) -> List[Dict]:
        """Generate quarterly cash flow data"""
        flows = []
        revenue = profile["revenue"]

        for i in range(4):
            quarter = f"2024-Q{4-i}"

            quarterly_revenue = revenue / 4
            net_income = int(quarterly_revenue * random.uniform(0.08, 0.25))

            flows.append(
                {
                    "ticker": ticker,
                    "quarter": quarter,
                    "operating_cash_flow": int(net_income * random.uniform(1.1, 1.4)),
                    "net_income": net_income,
                    "depreciation": int(quarterly_revenue * random.uniform(0.02, 0.05)),
                    "changes_in_working_capital": int(
                        net_income * random.uniform(-0.2, 0.2)
                    ),
                    "investing_cash_flow": int(net_income * random.uniform(-0.5, -0.2)),
                    "capex": int(quarterly_revenue * random.uniform(0.03, 0.08)),
                    "acquisitions": int(net_income * random.uniform(0, 0.3)),
                    "financing_cash_flow": int(net_income * random.uniform(-0.3, 0.3)),
                    "dividends_paid": int(net_income * random.uniform(0.2, 0.4)),
                    "stock_buyback": int(net_income * random.uniform(0, 0.5)),
                    "debt_issued": int(quarterly_revenue * random.uniform(0, 0.1)),
                    "debt_repaid": int(quarterly_revenue * random.uniform(0, 0.1)),
                    "free_cash_flow": int(net_income * random.uniform(0.8, 1.2)),
                    "filing_date": (datetime.now() - timedelta(days=90 * i)).date(),
                }
            )

        return flows

    def _generate_earnings(self, ticker: str, profile: Dict) -> List[Dict]:
        """Generate earnings data"""
        earnings = []

        for i in range(4):
            quarter = f"2024-Q{4-i}"
            eps_est = round(random.uniform(1.0, 5.0), 2)
            eps_actual = round(eps_est * random.uniform(0.95, 1.10), 2)

            revenue_est = int(profile["revenue"] / 4 * random.uniform(0.95, 1.05))
            revenue_actual = int(revenue_est * random.uniform(0.97, 1.08))

            earnings.append(
                {
                    "ticker": ticker,
                    "quarter": quarter,
                    "eps_reported": eps_actual,
                    "eps_estimated": eps_est,
                    "eps_surprise": round(((eps_actual - eps_est) / eps_est) * 100, 2),
                    "revenue_reported": revenue_actual,
                    "revenue_estimated": revenue_est,
                    "revenue_surprise": round(
                        ((revenue_actual - revenue_est) / revenue_est) * 100, 2
                    ),
                    "next_quarter_eps_guidance": round(
                        eps_actual * random.uniform(1.02, 1.08), 2
                    ),
                    "next_quarter_revenue_guidance": int(
                        revenue_actual * random.uniform(1.03, 1.10)
                    ),
                    "earnings_date": (datetime.now() - timedelta(days=90 * i)).date(),
                }
            )

        return earnings

    def _generate_sec_filings(self, ticker: str, profile: Dict) -> List[Dict]:
        """Generate SEC filings"""
        filings = []

        filing_types = [
            ("10-K", "Annual Report", 365),
            ("10-Q", "Quarterly Report Q3", 90),
            ("10-Q", "Quarterly Report Q2", 180),
            ("8-K", "Current Report - Earnings Release", 90),
        ]

        for filing_type, title, days_ago in filing_types:
            filings.append(
                {
                    "ticker": ticker,
                    "filing_type": filing_type,
                    "filing_date": (datetime.now() - timedelta(days=days_ago)).date(),
                    "title": f"{profile['name']} - {title}",
                    "summary": f"Filed {filing_type} for {profile['name']}. Contains financial statements, management discussion, and risk factors.",
                    "risk_factors": f"Risks include market volatility, competitive pressures, regulatory changes, economic conditions affecting {profile['sector']} sector, and operational challenges.",
                    "management_discussion": f"Management discusses strong performance in {profile['industry']} segment. Revenue growth of {profile['growth_rate']*100:.1f}% driven by market expansion and operational efficiency.",
                    "accession_number": f"0001{random.randint(100000, 999999)}-{random.randint(10, 99)}-{random.randint(100000, 999999)}",
                    "url": f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}",
                }
            )

        return filings

    def _generate_options_data(
        self, ticker: str, profile: Dict, days: int
    ) -> List[Dict]:
        """Generate options market data"""
        options = []

        for i in range(0, days, 7):  # Weekly data
            date = (datetime.now() - timedelta(days=days - i)).date()

            # Skip weekends
            if date.weekday() >= 5:
                continue

            options.append(
                {
                    "ticker": ticker,
                    "date": date,
                    "put_call_ratio": round(random.uniform(0.6, 1.2), 2),
                    "total_call_volume": random.randint(10000, 100000),
                    "total_put_volume": random.randint(8000, 90000),
                    "total_call_open_interest": random.randint(50000, 500000),
                    "total_put_open_interest": random.randint(40000, 450000),
                    "iv_30d": round(
                        profile["volatility"] * 100 * random.uniform(15, 25), 2
                    ),
                    "iv_60d": round(
                        profile["volatility"] * 100 * random.uniform(16, 26), 2
                    ),
                    "iv_90d": round(
                        profile["volatility"] * 100 * random.uniform(17, 27), 2
                    ),
                }
            )

        return options

    def _generate_macro_data(self, days: int) -> List[Dict]:
        """Generate macroeconomic indicators"""
        macro = []

        base_values = {
            "fed_funds_rate": 5.25,
            "treasury_10y": 4.50,
            "treasury_2y": 4.80,
            "gdp_growth": 2.5,
            "unemployment_rate": 3.8,
            "inflation_rate": 3.2,
            "cpi": 310.5,
            "ppi": 250.3,
            "sp500_level": 4500,
            "vix_level": 15.0,
            "oil_price": 75.0,
            "gold_price": 2000.0,
            "dxy": 103.5,
        }

        for i in range(0, days, 7):  # Weekly macro data
            date = (datetime.now() - timedelta(days=days - i)).date()

            # Small random walks from base values
            macro.append(
                {
                    "date": date,
                    "fed_funds_rate": round(
                        base_values["fed_funds_rate"] + random.uniform(-0.1, 0.1), 2
                    ),
                    "treasury_10y": round(
                        base_values["treasury_10y"] + random.uniform(-0.15, 0.15), 2
                    ),
                    "treasury_2y": round(
                        base_values["treasury_2y"] + random.uniform(-0.15, 0.15), 2
                    ),
                    "gdp_growth": round(
                        base_values["gdp_growth"] + random.uniform(-0.2, 0.2), 2
                    ),
                    "unemployment_rate": round(
                        base_values["unemployment_rate"] + random.uniform(-0.1, 0.1), 2
                    ),
                    "inflation_rate": round(
                        base_values["inflation_rate"] + random.uniform(-0.2, 0.2), 2
                    ),
                    "cpi": round(
                        base_values["cpi"] * (1 + random.uniform(-0.01, 0.01)), 2
                    ),
                    "ppi": round(
                        base_values["ppi"] * (1 + random.uniform(-0.01, 0.01)), 2
                    ),
                    "sp500_level": round(
                        base_values["sp500_level"] * (1 + random.uniform(-0.02, 0.02)),
                        2,
                    ),
                    "sp500_change": round(random.uniform(-2, 2), 2),
                    "vix_level": round(
                        base_values["vix_level"] * (1 + random.uniform(-0.15, 0.15)), 2
                    ),
                    "oil_price": round(
                        base_values["oil_price"] * (1 + random.uniform(-0.03, 0.03)), 2
                    ),
                    "gold_price": round(
                        base_values["gold_price"] * (1 + random.uniform(-0.02, 0.02)), 2
                    ),
                    "dxy": round(
                        base_values["dxy"] * (1 + random.uniform(-0.01, 0.01)), 2
                    ),
                }
            )

        return macro

    def _generate_news(self, ticker: str, profile: Dict, days: int) -> List[Dict]:
        """Generate news with categories"""
        news = []
        categories = ["earnings", "product", "regulatory", "market", "leadership"]

        news_templates = {
            "earnings": {
                "positive": [
                    f"{profile['name']} reports Q{{q}} earnings beat, revenue up {{pct}}%",
                    f"{profile['name']} exceeds analyst expectations in Q{{q}}",
                    f"Strong quarterly results from {profile['name']}",
                ],
                "negative": [
                    f"{profile['name']} misses Q{{q}} revenue expectations",
                    f"Weak guidance from {profile['name']} pressures stock",
                    f"{profile['name']} reports disappointing earnings",
                ],
                "neutral": [
                    f"{profile['name']} to report Q{{q}} earnings on {{date}}",
                    f"Analysts preview {profile['name']} earnings report",
                ],
            },
            "product": {
                "positive": [
                    f"{profile['name']} announces new product line expansion",
                    f"Strong demand for {profile['name']}'s latest offerings",
                    f"{profile['name']} launches innovative new product",
                ],
                "negative": [
                    f"{profile['name']} delays product launch",
                    f"Product recall affects {profile['name']}",
                ],
                "neutral": [
                    f"{profile['name']} updates product roadmap",
                ],
            },
            "regulatory": {
                "positive": [
                    f"Regulatory approval boosts {profile['name']}",
                    f"{profile['name']} wins regulatory battle",
                ],
                "negative": [
                    f"Regulatory scrutiny intensifies for {profile['name']}",
                    f"{profile['name']} faces compliance investigation",
                ],
                "neutral": [
                    f"Regulatory update affects {profile['name']}",
                ],
            },
            "market": {
                "positive": [
                    f"{profile['name']} stock surges on market optimism",
                    f"Analyst upgrades {profile['name']} target price",
                ],
                "negative": [
                    f"{profile['name']} stock drops on market concerns",
                    f"Bearish sentiment weighs on {profile['name']}",
                ],
                "neutral": [
                    f"{profile['name']} stock moves with broader market",
                ],
            },
            "leadership": {
                "positive": [
                    f"{profile['name']} appoints new CFO with strong track record",
                    f"Leadership change energizes {profile['name']}",
                ],
                "negative": [
                    f"{profile['name']} CEO departure surprises investors",
                ],
                "neutral": [
                    f"{profile['name']} executive changes announced",
                ],
            },
        }

        for _ in range(random.randint(15, 25)):
            category = random.choice(categories)

            # Sentiment based on trend
            if profile["trend"] == "bullish":
                sentiment_weights = {"positive": 0.6, "neutral": 0.3, "negative": 0.1}
            elif profile["trend"] == "bearish":
                sentiment_weights = {"positive": 0.1, "neutral": 0.3, "negative": 0.6}
            else:
                sentiment_weights = {
                    "positive": 0.33,
                    "neutral": 0.34,
                    "negative": 0.33,
                }

            sentiment = random.choices(
                list(sentiment_weights.keys()), weights=list(sentiment_weights.values())
            )[0]

            # Get headline template
            templates = news_templates[category].get(
                sentiment, news_templates[category]["neutral"]
            )
            headline = random.choice(templates).format(
                q=random.randint(1, 4),
                pct=random.randint(5, 25),
                date=datetime.now().strftime("%Y-%m-%d"),
            )

            # Sentiment scores
            sentiment_scores = {
                "positive": random.uniform(0.5, 0.9),
                "negative": random.uniform(-0.9, -0.5),
                "neutral": random.uniform(-0.2, 0.2),
            }

            news.append(
                {
                    "ticker": ticker,
                    "headline": headline,
                    "summary": f"Detailed analysis of {profile['name']} in {category} category. Market implications discussed.",
                    "sentiment": sentiment,
                    "sentiment_score": round(sentiment_scores[sentiment], 3),
                    "sentiment_confidence": round(random.uniform(0.7, 0.95), 3),
                    "category": category,
                    "relevance_score": round(random.uniform(0.7, 1.0), 3),
                    "published_at": datetime.now()
                    - timedelta(days=random.randint(0, days)),
                    "source": random.choice(
                        ["Reuters", "Bloomberg", "CNBC", "WSJ", "MarketWatch"]
                    ),
                    "author": f"{random.choice(['John', 'Jane', 'Mike', 'Sarah'])} {random.choice(['Smith', 'Doe', 'Johnson', 'Williams'])}",
                    "url": f"https://news.example.com/{ticker.lower()}-{category}",
                }
            )

        return news

    def _generate_analyst_ratings(self, ticker: str, profile: Dict) -> List[Dict]:
        """Generate analyst ratings"""
        ratings = []
        rating_types = ["strong buy", "buy", "hold", "sell", "strong sell"]
        firms = [
            "Goldman Sachs",
            "Morgan Stanley",
            "JP Morgan",
            "Bank of America",
            "Citigroup",
            "Wells Fargo",
            "Deutsche Bank",
            "Barclays",
            "UBS",
            "Credit Suisse",
            "Jefferies",
            "Piper Sandler",
        ]

        for _ in range(random.randint(8, 15)):
            rating = random.choices(rating_types, weights=[0.2, 0.3, 0.35, 0.1, 0.05])[
                0
            ]

            current_price = sum(profile["price_range"]) / 2
            if "buy" in rating:
                target = current_price * random.uniform(1.1, 1.3)
            elif "sell" in rating:
                target = current_price * random.uniform(0.7, 0.9)
            else:
                target = current_price * random.uniform(0.95, 1.05)

            ratings.append(
                {
                    "ticker": ticker,
                    "analyst_firm": random.choice(firms),
                    "analyst_name": f"{random.choice(['John', 'Jane', 'Michael', 'Sarah'])} {random.choice(['Smith', 'Johnson', 'Williams', 'Brown'])}",
                    "rating": rating,
                    "rating_change": random.choice(
                        ["upgrade", "downgrade", "maintain", None]
                    ),
                    "price_target": round(target, 2),
                    "previous_price_target": round(
                        target * random.uniform(0.95, 1.05), 2
                    ),
                    "rating_date": datetime.now()
                    - timedelta(days=random.randint(0, 90)),
                }
            )

        return ratings

    def _generate_insider_trades(self, ticker: str, profile: Dict) -> List[Dict]:
        """Generate insider trades"""
        trades = []

        insiders = [
            ("CEO", ["buy", "sell"], [0.3, 0.7]),
            ("CFO", ["buy", "sell"], [0.4, 0.6]),
            ("COO", ["buy", "sell"], [0.4, 0.6]),
            ("Director", ["buy", "sell"], [0.5, 0.5]),
            ("VP", ["buy", "sell"], [0.4, 0.6]),
        ]

        for _ in range(random.randint(8, 18)):
            title, types, weights = random.choice(insiders)
            transaction_type = random.choices(types, weights=weights)[0]
            shares = random.randint(1000, 100000)
            price = random.uniform(*profile["price_range"])

            trades.append(
                {
                    "ticker": ticker,
                    "insider_name": f"{random.choice(['John', 'Jane', 'Robert', 'Mary'])} {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Davis'])}",
                    "insider_title": title,
                    "transaction_type": transaction_type,
                    "shares": shares,
                    "price_per_share": round(price, 2),
                    "transaction_value": int(shares * price),
                    "transaction_date": datetime.now()
                    - timedelta(days=random.randint(0, 90)),
                    "filing_date": datetime.now()
                    - timedelta(days=random.randint(0, 92)),
                }
            )

        return trades

    def insert_to_database(self, db_connection):
        """Insert all generated data into database"""
        if not hasattr(db_connection, "cursor"):
            logger.error("Not a PostgreSQL connection")
            return False

        cursor = db_connection.cursor()

        try:
            # Insert fundamentals
            logger.info("Inserting fundamentals...")
            for fund in self.data["fundamentals"]:
                cursor.execute(
                    """
                    INSERT INTO mock_fundamentals 
                    (ticker, company_name, sector, industry, market_cap, enterprise_value,
                     pe_ratio, forward_pe, peg_ratio, pb_ratio, ps_ratio, pcf_ratio,
                     dividend_yield, earnings_per_share, revenue, revenue_growth, net_income,
                     profit_margin, operating_margin, gross_margin, roe, roa, roic,
                     debt_to_equity, current_ratio, quick_ratio, cash_ratio, interest_coverage,
                     asset_turnover, inventory_turnover, earnings_growth, book_value_per_share,
                     beta, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ticker) DO UPDATE SET
                        market_cap = EXCLUDED.market_cap,
                        pe_ratio = EXCLUDED.pe_ratio,
                        updated_at = EXCLUDED.updated_at
                """,
                    (
                        fund["ticker"],
                        fund["company_name"],
                        fund["sector"],
                        fund["industry"],
                        fund["market_cap"],
                        fund["enterprise_value"],
                        fund["pe_ratio"],
                        fund["forward_pe"],
                        fund["peg_ratio"],
                        fund["pb_ratio"],
                        fund["ps_ratio"],
                        fund["pcf_ratio"],
                        fund["dividend_yield"],
                        fund["earnings_per_share"],
                        fund["revenue"],
                        fund["revenue_growth"],
                        fund["net_income"],
                        fund["profit_margin"],
                        fund["operating_margin"],
                        fund["gross_margin"],
                        fund["roe"],
                        fund["roa"],
                        fund["roic"],
                        fund["debt_to_equity"],
                        fund["current_ratio"],
                        fund["quick_ratio"],
                        fund["cash_ratio"],
                        fund["interest_coverage"],
                        fund["asset_turnover"],
                        fund["inventory_turnover"],
                        fund["earnings_growth"],
                        fund["book_value_per_share"],
                        fund["beta"],
                        fund["updated_at"],
                    ),
                )

            # Insert prices
            logger.info("Inserting prices...")
            for price in self.data["prices"]:
                cursor.execute(
                    """
                    INSERT INTO mock_prices 
                    (ticker, date, open, high, low, close, volume, vwap)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ticker, date) DO UPDATE SET
                        close = EXCLUDED.close,
                        volume = EXCLUDED.volume
                """,
                    (
                        price["ticker"],
                        price["date"],
                        price["open"],
                        price["high"],
                        price["low"],
                        price["close"],
                        price["volume"],
                        price["vwap"],
                    ),
                )

            # Insert technical indicators
            logger.info("Inserting technical indicators...")
            for ind in self.data["technical_indicators"]:
                cursor.execute(
                    """
                    INSERT INTO mock_technical_indicators 
                    (ticker, date, sma_20, sma_50, sma_200, ema_12, ema_26,
                     rsi_14, macd, macd_signal, macd_histogram,
                     bollinger_upper, bollinger_middle, bollinger_lower,
                     atr_14, obv, adx_14)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ticker, date) DO NOTHING
                """,
                    (
                        ind["ticker"],
                        ind["date"],
                        ind["sma_20"],
                        ind["sma_50"],
                        ind["sma_200"],
                        ind["ema_12"],
                        ind["ema_26"],
                        ind["rsi_14"],
                        ind["macd"],
                        ind["macd_signal"],
                        ind["macd_histogram"],
                        ind["bollinger_upper"],
                        ind["bollinger_middle"],
                        ind["bollinger_lower"],
                        ind["atr_14"],
                        ind["obv"],
                        ind["adx_14"],
                    ),
                )

            # Insert risk metrics
            logger.info("Inserting risk metrics...")
            for risk in self.data["risk_metrics"]:
                cursor.execute(
                    """
                    INSERT INTO mock_risk_metrics 
                    (ticker, date, historical_volatility_30d, historical_volatility_90d,
                     implied_volatility, value_at_risk_95, value_at_risk_99, max_drawdown,
                     return_1d, return_1w, return_1m, return_3m, return_ytd,
                     sharpe_ratio, sortino_ratio, correlation_sp500)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ticker, date) DO NOTHING
                """,
                    (
                        risk["ticker"],
                        risk["date"],
                        risk["historical_volatility_30d"],
                        risk["historical_volatility_90d"],
                        risk["implied_volatility"],
                        risk["value_at_risk_95"],
                        risk["value_at_risk_99"],
                        risk["max_drawdown"],
                        risk["return_1d"],
                        risk["return_1w"],
                        risk["return_1m"],
                        risk["return_3m"],
                        risk["return_ytd"],
                        risk["sharpe_ratio"],
                        risk["sortino_ratio"],
                        risk["correlation_sp500"],
                    ),
                )

            # Insert balance sheet
            logger.info("Inserting balance sheets...")
            for bs in self.data["balance_sheet"]:
                cursor.execute(
                    """
                    INSERT INTO mock_balance_sheet 
                    (ticker, quarter, total_assets, current_assets, cash_and_equivalents,
                     accounts_receivable, inventory, total_liabilities, current_liabilities,
                     long_term_debt, short_term_debt, shareholders_equity, retained_earnings,
                     filing_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ticker, quarter) DO NOTHING
                """,
                    (
                        bs["ticker"],
                        bs["quarter"],
                        bs["total_assets"],
                        bs["current_assets"],
                        bs["cash_and_equivalents"],
                        bs["accounts_receivable"],
                        bs["inventory"],
                        bs["total_liabilities"],
                        bs["current_liabilities"],
                        bs["long_term_debt"],
                        bs["short_term_debt"],
                        bs["shareholders_equity"],
                        bs["retained_earnings"],
                        bs["filing_date"],
                    ),
                )

            # Insert cash flow
            logger.info("Inserting cash flow...")
            for cf in self.data["cash_flow"]:
                cursor.execute(
                    """
                    INSERT INTO mock_cash_flow 
                    (ticker, quarter, operating_cash_flow, net_income, depreciation,
                     changes_in_working_capital, investing_cash_flow, capex, acquisitions,
                     financing_cash_flow, dividends_paid, stock_buyback, debt_issued,
                     debt_repaid, free_cash_flow, filing_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ticker, quarter) DO NOTHING
                """,
                    (
                        cf["ticker"],
                        cf["quarter"],
                        cf["operating_cash_flow"],
                        cf["net_income"],
                        cf["depreciation"],
                        cf["changes_in_working_capital"],
                        cf["investing_cash_flow"],
                        cf["capex"],
                        cf["acquisitions"],
                        cf["financing_cash_flow"],
                        cf["dividends_paid"],
                        cf["stock_buyback"],
                        cf["debt_issued"],
                        cf["debt_repaid"],
                        cf["free_cash_flow"],
                        cf["filing_date"],
                    ),
                )

            # Insert earnings
            logger.info("Inserting earnings...")
            for earn in self.data["earnings"]:
                cursor.execute(
                    """
                    INSERT INTO mock_earnings 
                    (ticker, quarter, eps_reported, eps_estimated, eps_surprise,
                     revenue_reported, revenue_estimated, revenue_surprise,
                     next_quarter_eps_guidance, next_quarter_revenue_guidance, earnings_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ticker, quarter) DO NOTHING
                """,
                    (
                        earn["ticker"],
                        earn["quarter"],
                        earn["eps_reported"],
                        earn["eps_estimated"],
                        earn["eps_surprise"],
                        earn["revenue_reported"],
                        earn["revenue_estimated"],
                        earn["revenue_surprise"],
                        earn["next_quarter_eps_guidance"],
                        earn["next_quarter_revenue_guidance"],
                        earn["earnings_date"],
                    ),
                )

            # Insert SEC filings
            logger.info("Inserting SEC filings...")
            for filing in self.data["sec_filings"]:
                cursor.execute(
                    """
                    INSERT INTO mock_sec_filings 
                    (ticker, filing_type, filing_date, title, summary, risk_factors,
                     management_discussion, accession_number, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        filing["ticker"],
                        filing["filing_type"],
                        filing["filing_date"],
                        filing["title"],
                        filing["summary"],
                        filing["risk_factors"],
                        filing["management_discussion"],
                        filing["accession_number"],
                        filing["url"],
                    ),
                )

            # Insert options data
            logger.info("Inserting options data...")
            for opt in self.data["options_data"]:
                cursor.execute(
                    """
                    INSERT INTO mock_options_data 
                    (ticker, date, put_call_ratio, total_call_volume, total_put_volume,
                     total_call_open_interest, total_put_open_interest,
                     iv_30d, iv_60d, iv_90d)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ticker, date) DO NOTHING
                """,
                    (
                        opt["ticker"],
                        opt["date"],
                        opt["put_call_ratio"],
                        opt["total_call_volume"],
                        opt["total_put_volume"],
                        opt["total_call_open_interest"],
                        opt["total_put_open_interest"],
                        opt["iv_30d"],
                        opt["iv_60d"],
                        opt["iv_90d"],
                    ),
                )

            # Insert macro indicators
            logger.info("Inserting macro indicators...")
            for macro in self.data["macro_indicators"]:
                cursor.execute(
                    """
                    INSERT INTO mock_macro_indicators 
                    (date, fed_funds_rate, treasury_10y, treasury_2y, gdp_growth,
                     unemployment_rate, inflation_rate, cpi, ppi, sp500_level,
                     sp500_change, vix_level, oil_price, gold_price, dxy)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (date) DO NOTHING
                """,
                    (
                        macro["date"],
                        macro["fed_funds_rate"],
                        macro["treasury_10y"],
                        macro["treasury_2y"],
                        macro["gdp_growth"],
                        macro["unemployment_rate"],
                        macro["inflation_rate"],
                        macro["cpi"],
                        macro["ppi"],
                        macro["sp500_level"],
                        macro["sp500_change"],
                        macro["vix_level"],
                        macro["oil_price"],
                        macro["gold_price"],
                        macro["dxy"],
                    ),
                )

            # Insert news
            logger.info("Inserting news...")
            for article in self.data["news"]:
                cursor.execute(
                    """
                    INSERT INTO mock_news 
                    (ticker, headline, summary, sentiment, sentiment_score,
                     sentiment_confidence, category, relevance_score, published_at,
                     source, author, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        article["ticker"],
                        article["headline"],
                        article["summary"],
                        article["sentiment"],
                        article["sentiment_score"],
                        article["sentiment_confidence"],
                        article["category"],
                        article["relevance_score"],
                        article["published_at"],
                        article["source"],
                        article["author"],
                        article["url"],
                    ),
                )

            # Insert analyst ratings
            logger.info("Inserting analyst ratings...")
            for rating in self.data["analyst_ratings"]:
                cursor.execute(
                    """
                    INSERT INTO mock_analyst_ratings 
                    (ticker, analyst_firm, analyst_name, rating, rating_change,
                     price_target, previous_price_target, rating_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        rating["ticker"],
                        rating["analyst_firm"],
                        rating["analyst_name"],
                        rating["rating"],
                        rating["rating_change"],
                        rating["price_target"],
                        rating["previous_price_target"],
                        rating["rating_date"],
                    ),
                )

            # Insert insider trades
            logger.info("Inserting insider trades...")
            for trade in self.data["insider_trades"]:
                cursor.execute(
                    """
                    INSERT INTO mock_insider_trades 
                    (ticker, insider_name, insider_title, transaction_type, shares,
                     price_per_share, transaction_value, transaction_date, filing_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        trade["ticker"],
                        trade["insider_name"],
                        trade["insider_title"],
                        trade["transaction_type"],
                        trade["shares"],
                        trade["price_per_share"],
                        trade["transaction_value"],
                        trade["transaction_date"],
                        trade["filing_date"],
                    ),
                )

            db_connection.commit()
            logger.info("✅ All data inserted successfully!")
            return True

        except Exception as e:
            logger.error(f"Error inserting data: {e}")
            db_connection.rollback()
            return False

        finally:
            cursor.close()
