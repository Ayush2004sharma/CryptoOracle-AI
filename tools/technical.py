import requests
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands


class TechnicalAnalystAgent:
    def __init__(self, coingecko_api_key: str = None):
        self.coingecko_api_key = coingecko_api_key
        self.base_url = "https://api.coingecko.com/api/v3"
        # Map common coin names to CoinGecko IDs
        self.coin_id_map = {
            "bitcoin": "bitcoin",
            "btc": "bitcoin",
            "ethereum": "ethereum",
            "eth": "ethereum",
            "solana": "solana",
            "sol": "solana",
            "ripple": "ripple",
            "xrp": "ripple",
            "cardano": "cardano",
            "ada": "cardano",
        }

    def fetch_ohlc_data(self, coin_id="bitcoin", vs_currency="usd", days=30):
        """Fetch OHLC data from CoinGecko."""
        coin_id = self.coin_id_map.get(coin_id.lower(), coin_id.lower())
        url = f"{self.base_url}/coins/{coin_id}/market_chart"
        params = {
            "vs_currency": vs_currency,
            "days": days,
            "x_cg_demo_api_key": self.coingecko_api_key,
        }
        headers = {"accept": "application/json"}
        try:
            response = requests.get(url, params=params, headers=headers, timeout=20)
            if response.status_code != 200:
                return {"error": f"Failed to fetch OHLC: {response.status_code}"}

            data = response.json()
            prices = data.get("prices", [])
            if not prices:
                return {"error": "No OHLC price data found."}
            df = pd.DataFrame(prices, columns=["timestamp", "close"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
            df.set_index("timestamp", inplace=True)
            df["close"] = pd.to_numeric(df["close"], errors="coerce")
            return df
        except Exception as e:
            return {"error": f"Failed to fetch OHLC data: {str(e)}"}

    def compute_indicators(self, df: pd.DataFrame):
        """Compute technical indicators (RSI, MACD, Bollinger Bands)."""
        try:
            close = df["close"]
            indicators = {}
            rsi_val = RSIIndicator(close=close, window=14).rsi().iloc[-1]
            indicators["rsi"] = round(float(rsi_val), 2) if pd.notna(rsi_val) else None
            macd_obj = MACD(close=close, window_slow=26, window_fast=12, window_sign=9)
            macd_line = macd_obj.macd().iloc[-1]
            macd_signal = macd_obj.macd_signal().iloc[-1]
            indicators["macd"] = round(float(macd_line), 4) if pd.notna(macd_line) else None
            indicators["macd_signal"] = (
                round(float(macd_signal), 4) if pd.notna(macd_signal) else None
            )
            bb = BollingerBands(close=close, window=20, window_dev=2)
            bb_lower = bb.bollinger_lband().iloc[-1]
            bb_mid = bb.bollinger_mavg().iloc[-1]
            bb_upper = bb.bollinger_hband().iloc[-1]
            indicators["bb_lower"] = round(float(bb_lower), 2) if pd.notna(bb_lower) else None
            indicators["bb_middle"] = round(float(bb_mid), 2) if pd.notna(bb_mid) else None
            indicators["bb_upper"] = round(float(bb_upper), 2) if pd.notna(bb_upper) else None
            last_close = close.iloc[-1]
            indicators["close"] = round(float(last_close), 2) if pd.notna(last_close) else None
            return indicators
        except Exception as e:
            return {"error": f"Failed to compute indicators: {str(e)}"}
