from flask import Flask, jsonify, request
from database import Connection
from filters import Always, Started, Finished, Paid, AwaitingPayment, Equals
from tables import Movies, Reservations

app = Flask(__name__)
cinema_db = Connection("movies.db")


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
    query = Movies.objects.action("select").filters(condition).finalize()
    return jsonify(query.execute())


@app.route("/reservations", methods=["GET"])
def list_reservations():
    condition = {
        "paid": Paid(),
        "non-paid": AwaitingPayment()
    }.get(request.args.get("filter"), Always())
    query = Reservations.objects.action("select").filters(condition).finalize()
    return jsonify(query.execute())


@app.route("/reservations/make", methods=["POST"])
def add_reservation():
    values = {
        "movie_id": int(request.form.get("movie_id")),
        "paid": request.form.get("paid") == "true"
    }
    query = Reservations.objects.action("insert").values(values).finalize()
    query.execute()
    return jsonify(success=True)


@app.route("/reservations/clear", methods=["POST"])
def clear_non_paid_reservations():
    condition = AwaitingPayment()
    if "id" in request.form:
        condition = Equals("id", int(request.form["id"]))
    query = Reservations.objects.action("delete").filters(condition).finalize()
    query.execute()
    return jsonify(success=True)


if __name__ == '__main__':
    app.run()
