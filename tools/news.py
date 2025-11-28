import requests
from datetime import datetime

# ✅ Mapping coin names to symbols for CryptoPanic
COIN_SYMBOL_MAP = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "ripple": "XRP",
    "tether": "USDT",
    "binance coin": "BNB",
    "solana": "SOL",
    "usd coin": "USDC",
    "dogecoin": "DOGE",
    "tron": "TRX",
    "cardano": "ADA",
    "hyperliquid": "HYPE",
    "stellar": "XLM",
    "sui": "SUI",
    "chainlink": "LINK",
    "hedera": "HBAR",
    "bitcoin cash": "BCH",
    "avalanche": "AVAX",
    "wrapped bitcoin": "WBTC",
    "toncoin": "TON",
    "polkadot": "DOT",
    # Add more as needed
}


class FinanceNewsAnalystAgent:
    def __init__(self, cryptopanic_api_key: str):
        self.api_key = cryptopanic_api_key
        self.base_url = "https://cryptopanic.com/api/developer/v2/posts/"

    def fetch_news(self, currencies=None, filter_type="hot", kind="news", public=True):
        """Fetch news articles for specific coin(s) or the whole market."""
        params = {
            "auth_token": self.api_key,
            "filter": filter_type,
            "kind": kind,
        }

        if public:
            params["public"] = "true"

        if currencies:
            # ✅ Map coin name to ticker symbol if available
            symbol = COIN_SYMBOL_MAP.get(currencies.lower(), currencies.upper())
            params["currencies"] = symbol

        try:
            response = requests.get(self.base_url, params=params)

            if response.status_code != 200:
                return {"error": f"API Error {response.status_code}: {response.text}"}

            results = response.json().get("results", [])
            parsed_news = []

            for post in results:
                title = post.get("title", "").strip()
                published = post.get("published_at")
                url = (
                    post.get("url")
                    or post.get("original_url")
                    or "https://cryptopanic.com/"
                )
                source = post.get("source", {}).get("title", "Unknown")

                if not title or not published:
                    continue

                pub_time = datetime.fromisoformat(
                    published.replace("Z", "+00:00")
                ).strftime("%b %d %Y %H:%M UTC")

                parsed_news.append(
                    {
                        "Title": title,
                        "Source": source,
                        "Published": pub_time,
                        "URL": url,
                    }
                )

            return (
                parsed_news
                if parsed_news
                else {"error": f"No news found for {currencies}"}
            )

        except Exception as e:
            return {"error": f"Failed to fetch news: {str(e)}"}
