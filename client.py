"""Клиент API CoinGecko: загрузка и разбор JSON с курсами."""
from __future__ import annotations
import json
import urllib.parse
import urllib.request
from config import API_URL, CRYPTOS, REQUEST_TIMEOUT_SEC

class CryptoRatesClient:
    """Клиент API: загрузка и разбор JSON с курсами."""
    def __init__(
        self,
        crypto_ids: dict[str, str] | None = None,
        api_url: str = API_URL,
        timeout: int = REQUEST_TIMEOUT_SEC,
    ) -> None:
        self.crypto_ids = crypto_ids or CRYPTOS
        self.api_url = api_url
        self.timeout = timeout

    def _build_url(self) -> str:
        """Собирает URL запроса с нужными параметрами."""
        params = urllib.parse.urlencode(
            {
                "ids": ",".join(self.crypto_ids.keys()),
                "vs_currencies": "usd",
            }
        )

        return f"{self.api_url}?{params}"

    def fetch_rates(self) -> dict[str, float]:
        """Запрашивает курсы у CoinGecko и возвращает словарь id → цена USD."""
        request = urllib.request.Request(
            self._build_url(),
            headers={"Accept": "application/json"},
        )

        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)

        rates: dict[str, float] = {}

        for crypto_id, title in self.crypto_ids.items():
            if crypto_id not in data or "usd" not in data[crypto_id]:
                raise KeyError(f"курс для {title} не найден")
            rates[crypto_id] = float(data[crypto_id]["usd"])

        return rates
