from flask import request
from functools import wraps
import requests


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        try:
            auth_response = requests.post("http://127.0.0.1:5004/login", data=request.form)
        except requests.exceptions.ConnectionError:
            return "Authentication service is down", 503
        if auth_response.status_code != 200:
            return auth_response.content
        auth_response = auth_response.json()
        response = f(*args, user_id=auth_response["id"], **kwargs)
        response.headers["token"] = auth_response["token"]
        return response
    return inner
