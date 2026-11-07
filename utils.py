# Вспомогательные функции форматирования.
def format_price(value: float) -> str:
    if value >= 1000:
        return f"{value:,.2f} USD"
    if value >= 1:
        return f"{value:.2f} USD"

    return f"{value:.6f} USD"
