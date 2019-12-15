import requests
from time import sleep


def fetch_service_1_data(old):
    url = "http://127.0.0.1:5001/search"
    result = []
    for i in range(3):
        try:
            result = requests.get(f"{url}").json()
            break
        except requests.exceptions.ConnectionError:
            sleep(2**i)
    return normalize(result) or old


def normalize(data):
    for row in data:
        row["service"] = 1
    return data
