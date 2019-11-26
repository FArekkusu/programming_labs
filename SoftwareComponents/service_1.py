import requests


def fetch_service_1_data():
    url = "http://127.0.0.1:5001/search"
    try:
        result = requests.get(f"{url}").json()
    except requests.exceptions.ConnectionError:
        result = []
    return normalize(result)


def normalize(data):
    for row in data:
        row["service"] = 1
    return data
