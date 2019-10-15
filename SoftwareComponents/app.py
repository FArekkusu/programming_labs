from flask import Flask, jsonify, request
import requests
from database import Connection
from filters import Always, Started, Finished, Paid, AwaitingPayment
from qb_facade import QBFacade

app = Flask(__name__)
cinema_db = Connection("movies.db")
MOVIES_SERVICE_1_BASE_URL = "http://127.0.0.1:5001"
MOVIES_SERVICE_2_BASE_URL = "http://127.0.0.1:5002"


@app.route("/")
def home():
    return "Running"


@app.route("/movies", methods=["GET"])
def list_movies():
    condition = {
        "past": Finished(),
        "current": Started() & ~Finished(),
        "future": ~Started()
    }.get(request.args.get("filter"), Always())
    result = QBFacade.list_movies(condition)
    try:
        service_1_result = requests.get(MOVIES_SERVICE_1_BASE_URL + "/search").json()
    except requests.exceptions.ConnectionError:
        service_1_result = []
    try:
        service_2_result = requests.get(MOVIES_SERVICE_2_BASE_URL + "/price-list").json()
    except requests.exceptions.ConnectionError:
        service_2_result = []
    response = {
        "own": result,
        "service_1": service_1_result,
        "service_2": service_2_result
    }
    return jsonify(response)


@app.route("/reservations", methods=["GET"])
def list_reservations():
    condition = {
        "paid": Paid(),
        "non-paid": AwaitingPayment()
    }.get(request.args.get("filter"), Always())
    result = QBFacade.list_reservations(condition)
    return jsonify(result)


@app.route("/reservations/make", methods=["POST"])
def add_reservation():
    values = {
        "movie_id": int(request.form.get("movie_id")),
        "paid": request.form.get("paid") == "true"
    }
    result = QBFacade.add_reservation(values)
    return jsonify(success=result)


@app.route("/reservations/clear", methods=["POST"])
def clear_non_paid_reservations():
    result = QBFacade.clear_non_paid_reservations()
    return jsonify(success=result)


if __name__ == '__main__':
    app.run()
