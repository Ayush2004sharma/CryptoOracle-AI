# tools/sentiment.py

import os
import re
import requests

try:
    import snscrape.modules.twitter as sntwitter
except ImportError:
    sntwitter = None
    print("[WARN] snscrape not installed. Twitter/X sentiment will be disabled.")


class SocialSentimentScraper:
    """
    Combined sentiment scraper that pulls:
    - News posts from CryptoPanic
    - Social chatter from Twitter/X via snscrape

    It exposes `get_cleaned_posts(coin_symbol)` which is used by the
    existing `get_reddit_sentiment_posts` tool, so the rest of the
    system does not need to change.
    """

    def __init__(self, cryptopanic_key: str | None = None):
        # Support both env names for safety
        self.cryptopanic_key = (
            cryptopanic_key
            or os.getenv("CRYPTO_PANIC_KEY")
            or os.getenv("CRYPTO_PANIC_API_KEY")
        )

    # ---------------- CryptoPanic (News) ---------------- #

    def fetch_cryptopanic_posts(self, coin_symbol: str, limit: int = 30):
        if not self.cryptopanic_key:
            print("[WARN] CRYPTO_PANIC_KEY not set. Skipping CryptoPanic news.")
            return []

        params = {
            "auth_token": self.cryptopanic_key,
            "currencies": coin_symbol,
            "filter": "important",
            "kind": "news",
        }

        try:
            res = requests.get(
                "https://cryptopanic.com/api/v1/posts/",
                params=params,
                timeout=10,
            )
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            print(f"[WARN] CryptoPanic fetch failed: {e}")
            return []

        posts = []
        for item in data.get("results", [])[:limit]:
            title = item.get("title") or ""
            body = item.get("description") or ""
            combined = f"{title}. {body}".strip()
            if combined:
                posts.append(combined)
        return posts

    # ---------------- Twitter/X (snscrape) ---------------- #

    def fetch_twitter_posts(self, coin_symbol: str, limit: int = 50):
        if sntwitter is None:
            return []

        query = f"{coin_symbol} crypto lang:en"
        posts = []
        try:
            for i, tweet in enumerate(
                sntwitter.TwitterSearchScraper(query).get_items()
            ):
                if i >= limit:
                    break
                content = getattr(tweet, "content", "")
                if content:
                    posts.append(content)
        except Exception as e:
            print(f"[WARN] Twitter/X scraping failed: {e}")
            return []

        return posts

    # ---------------- Cleaning & Public API ---------------- #

    def clean_posts(self, texts):
        cleaned = []
        for text in texts:
            # Remove URLs
            text = re.sub(r"http\S+|www\S+|https\S+", "", text)
            # Remove mentions and hashtags
            text = re.sub(r"@\w+|#\w+", "", text)
            # Normalize whitespace and truncate
            text = re.sub(r"\s+", " ", text).strip()[:500]
            if text:
                cleaned.append(text)
        return cleaned

    def get_cleaned_posts(self, coin_symbol: str):
        """
        Returns a list of cleaned text snippets combining:
        - CryptoPanic news (titles/descriptions)
        - Twitter/X posts

        This is used by the `get_reddit_sentiment_posts` tool, so the
        social media agent can keep working without any code changes.
        """
        crypto_news = self.fetch_cryptopanic_posts(coin_symbol)
        twitter_posts = self.fetch_twitter_posts(coin_symbol)

        combined = crypto_news + twitter_posts
        cleaned = self.clean_posts(combined)

        if not cleaned:
            return [
                "No recent posts found for this coin from CryptoPanic or Twitter/X."
            ]

        return cleaned
