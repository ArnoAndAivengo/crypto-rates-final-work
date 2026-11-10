"""Константы приложения: список монет и параметры API."""
CRYPTOS: dict[str, str] = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "tether": "Tether (USDT)",
    "binancecoin": "BNB (BNB)",
    "solana": "Solana (SOL)",
    "ripple": "XRP (XRP)",
    "cardano": "Cardano (ADA)",
    "dogecoin": "Dogecoin (DOGE)",
}

API_URL = "https://api.coingecko.com/api/v3/simple/price"
REQUEST_TIMEOUT_SEC = 10
