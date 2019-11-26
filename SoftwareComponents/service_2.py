import requests


def fetch_service_2_data():
    url = "http://127.0.0.1:5002/price-list"
    result = []
    page, empty = 1, False
    while not empty:
        try:
            page_result = requests.get(f"{url}?page={page}").json()
        except requests.exceptions.ConnectionError:
            page_result = []
        result.extend(page_result)
        page += 1
        empty = not page_result
    return normalize(result)


def normalize(data):
    for row in data:
        row["service"] = 2
        row["name"] = row["title"]
        del row["title"]
    return data
