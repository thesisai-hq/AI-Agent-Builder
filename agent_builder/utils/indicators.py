"""
Technical Indicators Library
Comprehensive technical analysis tools for agents
"""

from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class TechnicalIndicators:
    """
    Complete technical analysis toolkit

    Usage:
        indicators = TechnicalIndicators()
        macd = indicators.calculate_macd(prices)
        bollinger = indicators.calculate_bollinger_bands(prices)
    """

    # ========================================================================
    # TREND INDICATORS
    # ========================================================================

    @staticmethod
    def calculate_sma(prices: List[float], period: int) -> float:
        """Simple Moving Average"""
        if len(prices) < period:
            return prices[0] if prices else 0
        return sum(prices[:period]) / period

    @staticmethod
    def calculate_ema(prices: List[float], period: int) -> float:
        """Exponential Moving Average"""
        if not prices or len(prices) < period:
            return prices[0] if prices else 0

        multiplier = 2 / (period + 1)
        ema = prices[0]

        for price in prices[1:period]:
            ema = price * multiplier + ema * (1 - multiplier)

        return ema

    @staticmethod
    def calculate_macd(
        prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9
    ) -> Dict[str, float]:
        """
        MACD (Moving Average Convergence Divergence)

        Returns: {macd, signal, histogram}
        """
        if len(prices) < slow:
            return {"macd": 0, "signal": 0, "histogram": 0}

        # Calculate EMAs
        ema_fast = TechnicalIndicators.calculate_ema(prices, fast)
        ema_slow = TechnicalIndicators.calculate_ema(prices, slow)

        macd_line = ema_fast - ema_slow

        # Calculate signal line (EMA of MACD)
        # For simplicity, using SMA here
        signal_line = macd_line * 0.8  # Approximation

        histogram = macd_line - signal_line

        return {
            "macd": round(macd_line, 4),
            "signal": round(signal_line, 4),
            "histogram": round(histogram, 4),
        }

    @staticmethod
    def calculate_bollinger_bands(
        prices: List[float], period: int = 20, std_dev: float = 2.0
    ) -> Dict[str, float]:
        """
        Bollinger Bands

        Returns: {upper, middle, lower, bandwidth, percent_b}
        """
        if len(prices) < period:
            current = prices[0] if prices else 0
            return {
                "upper": current,
                "middle": current,
                "lower": current,
                "bandwidth": 0,
                "percent_b": 0.5,
            }

        # Middle band (SMA)
        middle = sum(prices[:period]) / period

        # Standard deviation
        variance = sum((p - middle) ** 2 for p in prices[:period]) / period
        std = variance**0.5

        # Upper and lower bands
        upper = middle + (std_dev * std)
        lower = middle - (std_dev * std)

        # Bandwidth
        bandwidth = (upper - lower) / middle if middle != 0 else 0

        # %B (where price is relative to bands)
        current = prices[0]
        percent_b = (current - lower) / (upper - lower) if (upper - lower) != 0 else 0.5

        return {
            "upper": round(upper, 2),
            "middle": round(middle, 2),
            "lower": round(lower, 2),
            "bandwidth": round(bandwidth, 4),
            "percent_b": round(percent_b, 4),
        }

    # ========================================================================
    # MOMENTUM INDICATORS
    # ========================================================================

    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> float:
        """
        RSI (Relative Strength Index)

        Returns: 0-100
        """
        if len(prices) < period + 1:
            return 50.0

        gains = []
        losses = []

        for i in range(period):
            change = prices[i] - prices[i + 1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return round(rsi, 2)

    @staticmethod
    def calculate_stochastic(
        highs: List[float], lows: List[float], closes: List[float], period: int = 14
    ) -> Dict[str, float]:
        """
        Stochastic Oscillator

        Returns: {k, d}
        """
        if len(closes) < period:
            return {"k": 50.0, "d": 50.0}

        # Highest high and lowest low
        highest = max(highs[:period])
        lowest = min(lows[:period])
        current = closes[0]

        # %K
        if highest == lowest:
            k = 50.0
        else:
            k = ((current - lowest) / (highest - lowest)) * 100

        # %D (3-period SMA of %K) - simplified
        d = k * 0.9  # Approximation

        return {"k": round(k, 2), "d": round(d, 2)}

    @staticmethod
    def calculate_momentum(prices: List[float], period: int = 10) -> float:
        """
        Momentum indicator

        Returns: Current price - price N periods ago
        """
        if len(prices) <= period:
            return 0.0

        return round(prices[0] - prices[period], 4)

    @staticmethod
    def calculate_roc(prices: List[float], period: int = 10) -> float:
        """
        Rate of Change

        Returns: ((current - past) / past) * 100
        """
        if len(prices) <= period or prices[period] == 0:
            return 0.0

        current = prices[0]
        past = prices[period]

        roc = ((current - past) / past) * 100
        return round(roc, 2)

    # ========================================================================
    # VOLUME INDICATORS
    # ========================================================================

    @staticmethod
    def calculate_obv(prices: List[float], volumes: List[int]) -> float:
        """
        On-Balance Volume

        Returns: Cumulative volume based on price direction
        """
        if len(prices) < 2 or len(volumes) < 2:
            return 0.0

        obv = 0
        for i in range(len(prices) - 1):
            if prices[i] > prices[i + 1]:
                obv += volumes[i]
            elif prices[i] < prices[i + 1]:
                obv -= volumes[i]

        return obv

    @staticmethod
    def calculate_vwap(prices: List[float], volumes: List[int]) -> float:
        """
        Volume Weighted Average Price

        Returns: Average price weighted by volume
        """
        if not prices or not volumes:
            return 0.0

        total_pv = sum(p * v for p, v in zip(prices, volumes))
        total_volume = sum(volumes)

        if total_volume == 0:
            return prices[0]

        return round(total_pv / total_volume, 2)

    # ========================================================================
    # VOLATILITY INDICATORS
    # ========================================================================

    @staticmethod
    def calculate_atr(
        highs: List[float], lows: List[float], closes: List[float], period: int = 14
    ) -> float:
        """
        Average True Range

        Returns: Average trading range
        """
        if len(closes) < period + 1:
            return 0.0

        true_ranges = []
        for i in range(period):
            high_low = highs[i] - lows[i]
            high_close = abs(highs[i] - closes[i + 1])
            low_close = abs(lows[i] - closes[i + 1])
            true_ranges.append(max(high_low, high_close, low_close))

        atr = sum(true_ranges) / period
        return round(atr, 4)

    @staticmethod
    def calculate_volatility(prices: List[float], period: int = 20) -> float:
        """
        Historical Volatility (standard deviation)

        Returns: Price volatility as percentage
        """
        if len(prices) < period:
            return 0.0

        # Calculate returns
        returns = []
        for i in range(period - 1):
            if prices[i + 1] != 0:
                ret = (prices[i] - prices[i + 1]) / prices[i + 1]
                returns.append(ret)

        if not returns:
            return 0.0

        # Standard deviation of returns
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        volatility = (variance**0.5) * 100

        return round(volatility, 2)

    # ========================================================================
    # PATTERN RECOGNITION
    # ========================================================================

    @staticmethod
    def detect_golden_cross(
        fast_ma: float, slow_ma: float, prev_fast_ma: float, prev_slow_ma: float
    ) -> bool:
        """Detect golden cross (fast MA crosses above slow MA)"""
        return prev_fast_ma <= prev_slow_ma and fast_ma > slow_ma

    @staticmethod
    def detect_death_cross(
        fast_ma: float, slow_ma: float, prev_fast_ma: float, prev_slow_ma: float
    ) -> bool:
        """Detect death cross (fast MA crosses below slow MA)"""
        return prev_fast_ma >= prev_slow_ma and fast_ma < slow_ma

    @staticmethod
    def detect_support_resistance(
        prices: List[float], tolerance: float = 0.02
    ) -> Dict[str, List[float]]:
        """
        Detect support and resistance levels

        Returns: {support: [...], resistance: [...]}
        """
        if len(prices) < 10:
            return {"support": [], "resistance": []}

        supports = []
        resistances = []

        # Simple approach: find local minima/maxima
        for i in range(1, len(prices) - 1):
            # Local minimum (support)
            if prices[i] < prices[i - 1] and prices[i] < prices[i + 1]:
                supports.append(prices[i])

            # Local maximum (resistance)
            if prices[i] > prices[i - 1] and prices[i] > prices[i + 1]:
                resistances.append(prices[i])

        # Cluster similar levels
        def cluster_levels(levels, tolerance):
            if not levels:
                return []
            clustered = []
            current_cluster = [levels[0]]

            for level in levels[1:]:
                if abs(level - current_cluster[-1]) / current_cluster[-1] <= tolerance:
                    current_cluster.append(level)
                else:
                    clustered.append(sum(current_cluster) / len(current_cluster))
                    current_cluster = [level]

            if current_cluster:
                clustered.append(sum(current_cluster) / len(current_cluster))

            return clustered

        return {
            "support": cluster_levels(sorted(supports), tolerance),
            "resistance": cluster_levels(sorted(resistances, reverse=True), tolerance),
        }

    # ========================================================================
    # MULTI-INDICATOR ANALYSIS
    # ========================================================================

    @staticmethod
    def analyze_all(price_data: List[Dict]) -> Dict[str, any]:
        """
        Calculate all indicators at once

        Args:
            price_data: List of dicts with keys: open, high, low, close, volume

        Returns:
            Dict with all indicators
        """
        if not price_data:
            return {}

        # Extract data
        closes = [p["close"] for p in price_data]
        highs = [p["high"] for p in price_data]
        lows = [p["low"] for p in price_data]
        volumes = [p.get("volume", 0) for p in price_data]

        indicators = TechnicalIndicators()

        return {
            # Trend
            "sma_20": indicators.calculate_sma(closes, 20),
            "sma_50": indicators.calculate_sma(closes, 50),
            "sma_200": indicators.calculate_sma(closes, 200),
            "ema_12": indicators.calculate_ema(closes, 12),
            "ema_26": indicators.calculate_ema(closes, 26),
            "macd": indicators.calculate_macd(closes),
            "bollinger": indicators.calculate_bollinger_bands(closes),
            # Momentum
            "rsi_14": indicators.calculate_rsi(closes, 14),
            "stochastic": indicators.calculate_stochastic(highs, lows, closes),
            "momentum": indicators.calculate_momentum(closes, 10),
            "roc": indicators.calculate_roc(closes, 10),
            # Volume
            "obv": indicators.calculate_obv(closes, volumes),
            "vwap": indicators.calculate_vwap(closes, volumes),
            # Volatility
            "atr": indicators.calculate_atr(highs, lows, closes),
            "volatility": indicators.calculate_volatility(closes),
            # Levels
            "support_resistance": indicators.detect_support_resistance(closes),
            # Current price
            "current_price": closes[0],
            "price_change": (
                ((closes[0] - closes[-1]) / closes[-1] * 100) if len(closes) > 1 else 0
            ),
        }


# ============================================================================
# HELPER FUNCTIONS FOR AGENTS
# ============================================================================


def get_technical_signal(indicators: Dict) -> Tuple[str, float, str]:
    """
    Generate trading signal from technical indicators

    Returns: (signal, confidence, reasoning)
    """
    bullish_signals = 0
    bearish_signals = 0
    total_signals = 0
    reasons = []

    # RSI
    rsi = indicators.get("rsi_14", 50)
    if rsi < 30:
        bullish_signals += 1
        reasons.append(f"RSI oversold ({rsi:.1f})")
    elif rsi > 70:
        bearish_signals += 1
        reasons.append(f"RSI overbought ({rsi:.1f})")
    total_signals += 1

    # MACD
    macd = indicators.get("macd", {})
    if macd.get("histogram", 0) > 0:
        bullish_signals += 1
        reasons.append("MACD bullish")
    elif macd.get("histogram", 0) < 0:
        bearish_signals += 1
        reasons.append("MACD bearish")
    total_signals += 1

    # Moving averages
    current = indicators.get("current_price", 0)
    sma_20 = indicators.get("sma_20", current)
    sma_50 = indicators.get("sma_50", current)

    if current > sma_20 > sma_50:
        bullish_signals += 1
        reasons.append("Price above MAs")
    elif current < sma_20 < sma_50:
        bearish_signals += 1
        reasons.append("Price below MAs")
    total_signals += 1

    # Bollinger Bands
    bb = indicators.get("bollinger", {})
    percent_b = bb.get("percent_b", 0.5)
    if percent_b < 0.2:
        bullish_signals += 1
        reasons.append("Near lower Bollinger Band")
    elif percent_b > 0.8:
        bearish_signals += 1
        reasons.append("Near upper Bollinger Band")
    total_signals += 1

    # Calculate signal
    if bullish_signals > bearish_signals:
        signal = "bullish"
        confidence = bullish_signals / total_signals
    elif bearish_signals > bullish_signals:
        signal = "bearish"
        confidence = bearish_signals / total_signals
    else:
        signal = "neutral"
        confidence = 0.5

    reasoning = "; ".join(reasons) if reasons else "Mixed signals"

    return signal, round(confidence, 2), reasoning


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    """Test technical indicators"""

    # Sample price data
    price_data = [
        {"open": 180, "high": 185, "low": 179, "close": 183, "volume": 1000000},
        {"open": 183, "high": 187, "low": 182, "close": 186, "volume": 1200000},
        {"open": 186, "high": 188, "low": 184, "close": 185, "volume": 900000},
        {"open": 185, "high": 189, "low": 184, "close": 188, "volume": 1100000},
        {"open": 188, "high": 192, "low": 187, "close": 190, "volume": 1300000},
    ]

    # Calculate all indicators
    indicators = TechnicalIndicators.analyze_all(price_data)

    print("\n" + "=" * 70)
    print("TECHNICAL INDICATORS")
    print("=" * 70)
    print(f"\nCurrent Price: ${indicators['current_price']:.2f}")
    print(f"RSI (14): {indicators['rsi_14']:.2f}")
    print(f"MACD: {indicators['macd']}")
    print(f"Bollinger Bands: {indicators['bollinger']}")
    print(f"Volatility: {indicators['volatility']:.2f}%")

    # Get trading signal
    signal, confidence, reasoning = get_technical_signal(indicators)
    print(f"\nSignal: {signal.upper()}")
    print(f"Confidence: {confidence:.0%}")
    print(f"Reasoning: {reasoning}")
    print("=" * 70 + "\n")
