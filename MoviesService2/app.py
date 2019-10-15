from flask import Flask, jsonify
from database import Connection
from filters import Equals
from qb_facade import QBFacade

app = Flask(__name__)
cinema_db = Connection("movies.db")


@app.route("/")
def home():
    return "Running"


@app.route("/price-list", methods=["GET"])
def list_movies():
    result = QBFacade.list_movies()
    return jsonify(result)


@app.route("/details/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    result = QBFacade.get_movie(Equals("id", movie_id))
    return jsonify(result)


if __name__ == '__main__':
    app.run()
