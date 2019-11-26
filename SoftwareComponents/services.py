from service_1 import fetch_service_1_data
from service_2 import fetch_service_2_data


FETCH_HANDLERS = [
    fetch_service_1_data,
    fetch_service_2_data
]


def make_requests_to_services():
    result = []
    for handler in FETCH_HANDLERS:
        result.extend(handler())
    return result
