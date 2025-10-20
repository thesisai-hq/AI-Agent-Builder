import pandas as pd
from typing import List, Dict


def calculate_technical_indicators(stock_prices: List[Dict]) -> Dict:
    """
    Calculate technical indicators from raw stock_prices table

    Args:
        stock_prices: List from database with keys: date, open, high, low, close, volume

    Returns:
        Dict with all technical indicators
    """
    df = pd.DataFrame(stock_prices)
    df = df.sort_values("date")

    # Moving Averages
    df["sma_20"] = df["close"].rolling(window=20).mean()
    df["sma_50"] = df["close"].rolling(window=50).mean()
    df["sma_200"] = df["close"].rolling(window=200).mean()

    df["ema_12"] = df["close"].ewm(span=12).mean()
    df["ema_26"] = df["close"].ewm(span=26).mean()

    # RSI
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["rsi_14"] = 100 - (100 / (1 + rs))

    # MACD
    df["macd"] = df["ema_12"] - df["ema_26"]
    df["macd_signal"] = df["macd"].ewm(span=9).mean()
    df["macd_histogram"] = df["macd"] - df["macd_signal"]

    # Bollinger Bands
    df["bb_middle"] = df["close"].rolling(window=20).mean()
    bb_std = df["close"].rolling(window=20).std()
    df["bb_upper"] = df["bb_middle"] + (bb_std * 2)
    df["bb_lower"] = df["bb_middle"] - (bb_std * 2)

    # Volume indicators
    df["volume_sma"] = df["volume"].rolling(window=20).mean()

    return df.to_dict("records")
