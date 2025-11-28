import requests


class FundamentalAnalystAgent:
    def __init__(self, coingecko_api_key: str = None):
        self.coingecko_api_key = coingecko_api_key
        self.base_url = "https://api.coingecko.com/api/v3"
        # Map common coin names to CoinGecko IDs
        self.coin_id_map = {
            "bitcoin": "bitcoin",
            "btc": "bitcoin",
            "ethereum": "ethereum",
            "eth": "ethereum",
            "xrp": "ripple",
            "ripple": "ripple",
            "tether": "tether",
            "usdt": "tether",
            "binance coin": "binancecoin",
            "bnb": "binancecoin",
            "solana": "solana",
            "sol": "solana",
            "usd coin": "usd-coin",
            "usdc": "usd-coin",
            "dogecoin": "dogecoin",
            "doge": "dogecoin",
            "tron": "tron",
            "trx": "tron",
            "cardano": "cardano",
            "ada": "cardano",
            "hyperliquid": "hyperliquid",
            "hype": "hyperliquid",
            "stellar": "stellar",
            "xlm": "stellar",
            "sui": "sui",
            "chainlink": "chainlink",
            "link": "chainlink",
            "hedera": "hedera",
            "hbar": "hedera",
            "bitcoin cash": "bitcoin-cash",
            "bch": "bitcoin-cash",
            "avalanche": "avalanche",
            "avax": "avalanche",
            "wrapped bitcoin": "wrapped-bitcoin",
            "wbtc": "wrapped-bitcoin",
            "toncoin": "toncoin",
            "ton": "toncoin",
            "polkadot": "polkadot",
            "dot": "polkadot",
        }

    def fetch_data(self, coin_id: str) -> dict:
        """Return fundamental metrics from CoinGecko."""
        # Normalize coin_id
        coin_id = self.coin_id_map.get(coin_id.lower(), coin_id.lower())
        params = {"localization": "false", "x_cg_demo_api_key": self.coingecko_api_key}
        try:
            coin_resp = requests.get(f"{self.base_url}/coins/{coin_id}", params=params)
            tickers_resp = requests.get(
                f"{self.base_url}/coins/{coin_id}/tickers", params=params
            )

            if coin_resp.status_code != 200:
                return {"error": f"Coin data failed: {coin_resp.status_code}"}
            if tickers_resp.status_code != 200:
                return {"warning": f"Ticker data failed: {tickers_resp.status_code}"}

            coin_data = coin_resp.json()
            tickers_data = tickers_resp.json()

            return {
                "Name": coin_data.get("name", "Unknown"),
                "Symbol": coin_data.get("symbol", "").upper(),
                "Market Cap (USD)": coin_data.get("market_data", {})
                .get("market_cap", {})
                .get("usd", 0),
                "Circulating Supply": coin_data.get("market_data", {}).get(
                    "circulating_supply", 0
                ),
                "Total Supply": coin_data.get("market_data", {}).get("total_supply", 0),
                "TVL (USD)": coin_data.get("market_data", {}).get(
                    "total_value_locked", None
                ),
                "Token Categories": coin_data.get("categories") or [],
                "Token Platforms": coin_data.get("platforms") or {},
                "Exchange Listings Count": len(tickers_data.get("tickers", [])),
            }

        except Exception as e:
            return {"error": f"Failed to fetch data: {str(e)}"}
