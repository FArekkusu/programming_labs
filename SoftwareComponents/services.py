from service_1 import fetch_service_1_data
from service_2 import fetch_service_2_data


FETCH_HANDLERS = [
    (fetch_service_1_data, "service_1"),
    (fetch_service_2_data, "service_2")
]


def make_requests_to_services(cache):
    result = []
    for (handler, key) in FETCH_HANDLERS:
        cache.set(key, handler(cache.get(key) or []))
    return result
