# toolkit/crypto_tools_wrapped.py

from pydantic import BaseModel
from langchain_core.tools import tool
import json

# Global reference to shared tool instances (agents/scrapers)
TOOLKIT_REF = {}


# Input schema for all tools
class CoinInput(BaseModel):
    coin: str


@tool(args_schema=CoinInput)
def get_crypto_news(coin: str) -> str:
    """Return recent news articles related to a cryptocurrency coin."""
    news = TOOLKIT_REF["news_agent"].fetch_news(currencies=coin)
    return json.dumps(news, indent=2)


@tool(args_schema=CoinInput)
def get_crypto_fundamentals(coin: str) -> str:
    """Fetch raw fundamental data for a cryptocurrency coin."""
    data = TOOLKIT_REF["fundamental_agent"].fetch_data(coin)
    return json.dumps(data, indent=2)


@tool(args_schema=CoinInput)
def get_crypto_technicals(coin: str) -> str:
    """Return technical indicators (RSI, MACD, Bollinger Bands) for a cryptocurrency coin."""
    df = TOOLKIT_REF["technical_agent"].fetch_ohlc_data(coin)
    if isinstance(df, dict) and "error" in df:
        return json.dumps(df)
    indicators = TOOLKIT_REF["technical_agent"].compute_indicators(df)
    return json.dumps(indicators, indent=2)


@tool(args_schema=CoinInput)
def get_reddit_sentiment_posts(coin: str) -> str:
    """
    Fetch cleaned social & news posts (Twitter/X + CryptoPanic)
    about a cryptocurrency for sentiment analysis.

    Kept under the old name for backward compatibility.
    """
    cleaned_posts = TOOLKIT_REF["reddit_scraper"].get_cleaned_posts(coin)
    return "\n\n".join(cleaned_posts[:20])
