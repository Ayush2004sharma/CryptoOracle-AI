# toolkit/crypto_toolkit.py

from tools.news import FinanceNewsAnalystAgent
from tools.fundamentals import FundamentalAnalystAgent
from tools.sentiment import SocialSentimentScraper
from tools.technical import TechnicalAnalystAgent

# Import wrapped tools and the global reference
from toolkit.crypto_tools_wrapped import (
    get_crypto_news,
    get_crypto_fundamentals,
    get_crypto_technicals,
    get_reddit_sentiment_posts,
    TOOLKIT_REF,
)


class MyCryptoToolKit:
    def __init__(
        self,
        cryptopanic_key,
        coingecko_key,
        reddit_id=None,
        reddit_secret=None,
        reddit_agent=None,
    ):
        # Create agent instances
        self.news_agent = FinanceNewsAnalystAgent(cryptopanic_key)
        self.fundamental_agent = FundamentalAnalystAgent(coingecko_key)
        self.technical_agent = TechnicalAnalystAgent(coingecko_key)

        # ✅ Social/news sentiment scraper (CryptoPanic + Twitter/X)
        # Kept under attribute name `reddit_scraper` for backward compatibility.
        self.reddit_scraper = SocialSentimentScraper(cryptopanic_key)

        # Inject them into global context for tools
        TOOLKIT_REF["news_agent"] = self.news_agent
        TOOLKIT_REF["fundamental_agent"] = self.fundamental_agent
        TOOLKIT_REF["technical_agent"] = self.technical_agent
        TOOLKIT_REF["reddit_scraper"] = self.reddit_scraper

        # Expose tools
        self.get_crypto_news = get_crypto_news
        self.get_crypto_fundamentals = get_crypto_fundamentals
        self.get_crypto_technicals = get_crypto_technicals
        self.get_reddit_sentiment_posts = get_reddit_sentiment_posts
