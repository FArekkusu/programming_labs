from flask import Flask, jsonify, request
import re
from time import sleep
from database import Connection
from filters import Always, Greater, Less, Equals, parse_date, normalize_string
from qb_facade import QBFacade

app = Flask(__name__)
cinema_db = Connection("movies.db")


@app.route("/")
def home():
    return "Running"


@app.route("/search", methods=["GET"])
def list_movies():
    condition = Always()
    for field, query in request.args.items():
        comparison, value = query[:2], query[4:]
        filter_condition = {"gt": Greater, "lt": Less, "eq": Equals}[comparison]
        function = parse_date if re.match(r"(\d\d-){2}\d{4}$", value) else int if re.match(r"\d+$", value) else normalize_string
        condition &= filter_condition(field, function(value), function=function)
    result = QBFacade.list_movies(condition)
    sleep(0.5)
    return jsonify(result)


@app.route("/generate-data/<int:n>", methods=["POST"])
def generate_data(n):
    from random import randint as R, choices as C
    from string import ascii_lowercase as AL
    from time import time as T

    return "NOT ALLOWED"

    rows = []
    for _ in range(n):
        name = "".join(C(AL, k=6)).title()
        price = R(7, 20) * 5
        runtime = R(75, 180)
        description = "".join(C(AL + " ", k=40))
        release_date = f"{R(1, 28):02}-{R(1, 12):02}-{R(1990, 2019)}"
        rows.append((name, price, runtime, description, release_date))
    start = T()
    with Connection() as c:
        c.executemany("INSERT INTO movies(name, price, runtime, description, release_date) VALUES (?,?,?,?,?)", rows)
    finish = T()
    return str(finish - start)


if __name__ == '__main__':
    app.run()
