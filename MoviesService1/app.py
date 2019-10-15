from flask import Flask, jsonify, request
import re
from database import Connection
from filters import Always, Greater, Less, Equals, parse_date
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
        function = parse_date if re.match(r"(\d\d-){2}\d{4}", value) else int
        condition &= filter_condition(field, function(value), function=function)
    result = QBFacade.list_movies(condition)
    return jsonify(result)


if __name__ == '__main__':
    app.run()
