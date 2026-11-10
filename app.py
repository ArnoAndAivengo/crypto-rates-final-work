"""Графический интерфейс приложения на tkinter."""
from __future__ import annotations
import json
import tkinter as tk
import urllib.error
from datetime import datetime
from tkinter import messagebox, ttk
from client import CryptoRatesClient
from utils import format_price

class CryptoRatesApp:
    """Графическое приложение на tkinter для отображения курсов."""
    def __init__(self, client: CryptoRatesClient | None = None) -> None:
        self.client = client or CryptoRatesClient()
        self.price_labels: dict[str, tk.Label] = {}

        self.window = tk.Tk()
        self.window.title("Курсы криптовалют")
        self.window.geometry("380x520")
        self.window.resizable(False, False)

        self._build_ui()

    def _build_ui(self) -> None:
        """Создаёт элементы интерфейса и раскладывает их по окну."""
        tk.Label(
            self.window,
            text="Курсы популярных криптовалют",
            font=("", 12, "bold"),
        ).pack(pady=(20, 5))

        tk.Label(
            self.window,
            text="относительно доллара США (USD)",
            font=("", 9),
            fg="gray",
        ).pack(pady=(0, 10))

        frame = ttk.Frame(self.window, padding=10)
        frame.pack(fill="both", expand=True, padx=20)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)

        for row, (crypto_id, title) in enumerate(self.client.crypto_ids.items()):
            tk.Label(frame, text=title, anchor="w").grid(
                row=row, column=0, sticky="w", pady=6
            )
            price = tk.Label(frame, text="- USD", anchor="e", width=14)
            price.grid(row=row, column=1, sticky="e", pady=6, padx=(10, 0))
            self.price_labels[crypto_id] = price

        self.status_label = tk.Label(
            self.window,
            text='Нажмите "Обновить курсы", чтобы загрузить данные',
            font=("", 8),
            fg="gray",
            wraplength=340,
        )
        self.status_label.pack(pady=(5, 0))

        self.refresh_button = tk.Button(
            self.window,
            text="Обновить курсы",
            command=self.update_rates,
            width=20,
        )
        self.refresh_button.pack(pady=18)

    def _set_status(self, text: str) -> None:
        """Обновляет строку статуса под списком курсов."""
        self.status_label.config(text=text)

    def _show_prices(self, rates: dict[str, float]) -> None:
        """Подставляет загруженные цены в метки интерфейса."""
        for crypto_id, price in rates.items():
            self.price_labels[crypto_id].config(text=format_price(price))

        now = datetime.now().strftime("%H:%M:%S")
        self._set_status(f"Обновлено: {now}")

    def update_rates(self) -> None:
        """Загружает курсы и обновляет интерфейс; показывает ошибки пользователю."""
        self.refresh_button.config(state="disabled")
        self._set_status("Загрузка данных…")
        self.window.update_idletasks()

        try:
            rates = self.client.fetch_rates()
        except urllib.error.URLError:
            messagebox.showerror(
                "Ошибка сети",
                "Не удалось подключиться к CoinGecko.\n"
                "Проверьте интернет-соединение и попробуйте снова.",
            )
            self._set_status("Ошибка сети. Повторите попытку.")
        except TimeoutError:
            messagebox.showerror(
                "Ошибка сети",
                "Превышено время ожидания ответа от сервера.",
            )
            self._set_status("Таймаут запроса. Повторите попытку.")
        except (KeyError, ValueError, TypeError, json.JSONDecodeError) as error:
            messagebox.showerror(
                "Ошибка данных",
                f"Не удалось разобрать ответ API:\n{error}",
            )
            self._set_status("Ошибка разбора JSON. Повторите попытку.")
        else:
            self._show_prices(rates)
        finally:
            self.refresh_button.config(state="normal")

    def run(self) -> None:
        self.window.mainloop()