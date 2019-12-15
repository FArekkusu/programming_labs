import requests
from time import sleep


def fetch_service_2_data(old):
    url = "http://127.0.0.1:5002/price-list"
    result = {row["id"]: row for row in old}
    page, empty = 1, False
    while not empty:
        page_result = []
        for i in range(3):
            try:
                page_result = requests.get(f"{url}?page={page}").json()
                break
            except requests.exceptions.ConnectionError:
                sleep(2**i)
        result.update({row["id"]: row for row in page_result})
        page += 1
        empty = not page_result
    return normalize([*result.values()])


def normalize(data):
    for row in data:
        row["service"] = 2
        if "title" in row:
            row["name"] = row["title"]
            del row["title"]
    return data
