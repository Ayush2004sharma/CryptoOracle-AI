export const COIN_CONFIG = {
  bitcoin: {
    label: "Bitcoin",
    short: "BTC",
    tv: "BINANCE:BTCUSDT",
  },
  ethereum: {
    label: "Ethereum",
    short: "ETH",
    tv: "BINANCE:ETHUSDT",
  },
  ripple: {
    label: "Ripple",
    short: "XRP",
    tv: "BINANCE:XRPUSDT",
  },
  tether: {
    label: "Tether",
    short: "USDT",
    tv: "BINANCE:USDTUSDT", // ⚠️ mostly useless as chart
  },
  "binance coin": {
    label: "BNB",
    short: "BNB",
    tv: "BINANCE:BNBUSDT",
  },
  solana: {
    label: "Solana",
    short: "SOL",
    tv: "BINANCE:SOLUSDT",
  },
  "usd coin": {
    label: "USDC",
    short: "USDC",
    tv: "BINANCE:USDCUSDT",
  },
  dogecoin: {
    label: "Dogecoin",
    short: "DOGE",
    tv: "BINANCE:DOGEUSDT",
  },
  tron: {
    label: "Tron",
    short: "TRX",
    tv: "BINANCE:TRXUSDT",
  },
  cardano: {
    label: "Cardano",
    short: "ADA",
    tv: "BINANCE:ADAUSDT",
  },
  hyperliquid: {
    label: "Hyperliquid",
    short: "HYPE",
    tv: "BINANCE:HYPEUSDT", // ⚠️ if not available, fallback needed
  },
  stellar: {
    label: "Stellar",
    short: "XLM",
    tv: "BINANCE:XLMUSDT",
  },
  sui: {
    label: "Sui",
    short: "SUI",
    tv: "BINANCE:SUIUSDT",
  },
  chainlink: {
    label: "Chainlink",
    short: "LINK",
    tv: "BINANCE:LINKUSDT",
  },
  hedera: {
    label: "Hedera",
    short: "HBAR",
    tv: "BINANCE:HBARUSDT",
  },
  "bitcoin cash": {
    label: "Bitcoin Cash",
    short: "BCH",
    tv: "BINANCE:BCHUSDT",
  },
  avalanche: {
    label: "Avalanche",
    short: "AVAX",
    tv: "BINANCE:AVAXUSDT",
  },
  "wrapped bitcoin": {
    label: "Wrapped Bitcoin",
    short: "WBTC",
    tv: "BINANCE:WBTCUSDT",
  },
  toncoin: {
    label: "Toncoin",
    short: "TON",
    tv: "BINANCE:TONUSDT",
  },
  polkadot: {
    label: "Polkadot",
    short: "DOT",
    tv: "BINANCE:DOTUSDT",
  },
} as const

export type SupportedCoin = keyof typeof COIN_CONFIG
