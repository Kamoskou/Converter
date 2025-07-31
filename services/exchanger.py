import requests

def get_rates(base_currency="USD"):
    url = f"https://open.er-api.com/v6/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    return data.get("rates", {})
