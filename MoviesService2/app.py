from flask import Flask, jsonify, request
from database import Connection
from filters import Equals
from qb_facade import QBFacade

app = Flask(__name__)
cinema_db = Connection("movies.db")

RECORDS_PER_PAGE = 100


@app.route("/")
def home():
    return "Running"


@app.route("/price-list", methods=["GET"])
def list_movies():
    try:
        page = int(request.args.get("page", 1))
        assert page > 0
    except (ValueError, AssertionError):
        page = 1
    right_bound = RECORDS_PER_PAGE * page
    left_bound = right_bound - RECORDS_PER_PAGE
    result = QBFacade.list_movies()[left_bound:right_bound]
    return jsonify(result)


@app.route("/details/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    result = QBFacade.get_movie(Equals("id", movie_id))
    return jsonify(result)


@app.route("/generate-data/<int:n>", methods=["POST"])
def generate_data(n):
    from random import randint as R, choices as C
    from string import ascii_lowercase as AL
    from time import time as T

    return "NOT ALLOWED"

    rows = []
    for _ in range(n):
        title = "".join(C(AL, k=6)).title()
        price = R(7, 20) * 5
        runtime = R(75, 180)
        description = "".join(C(AL + " ", k=40))
        release_date = f"{R(1, 28):02}-{R(1, 12):02}-{R(1990, 2019)}"
        rows.append((title, price, runtime, description, release_date))
    start = T()
    with Connection() as c:
        c.executemany("INSERT INTO movies(title, price, runtime, description, release_date) VALUES (?,?,?,?,?)", rows)
    finish = T()
    return str(finish - start)


if __name__ == '__main__':
    app.run()
