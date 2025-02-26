import requests


url = "https://www.cbr-xml-daily.ru/daily_json.js"

def get_usd_rate() -> float | None:
    """ Получение актуального на момент запроса курса доллара с сайта ЦБ РФ"""
    try:
        response = requests.get(url)
        status_code = response.status_code
        if status_code != 200:
            print(f"Ошибка получения курса USD status_code: {status_code}")
        else:
            result = response.json()
            rate_usd = result.get("Valute", {}).get("USD", {}).get("Value", 0.0)
            return rate_usd
    except ConnectionError:
        print("Курс доллара не получен")
        return None


if __name__ == "__main__":
    curs = get_usd_rate()
    print(curs)
