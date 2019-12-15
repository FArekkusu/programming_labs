from flask import Flask, jsonify, request, Response, redirect
from database import Connection
from decorators import login_required
import requests
from filters import Always, Paid, AwaitingPayment, Greater, Less, Equals, parse_date, normalize_string
from qb_facade import QBFacade


app = Flask(__name__)
cinema_db = Connection("reservations.db")


@app.route("/")
def home():
    return "Running"


@app.route("/list", methods=["POST"])
@login_required
def list_reservations(user_id):
    with Connection() as c:
        rows = c.execute("SELECT id, service_id, movie_id FROM reservations WHERE user_id = ?", (user_id, )).fetchall()
        headers = [x[0] for x in c.description]
    return jsonify([dict(zip(headers, row)) for row in rows])


@app.route("/create", methods=["POST"])
@login_required
def create_reservation(user_id):
    try:
        service_id = int(request.form.get("service_id"))
        movie_id = int(request.form.get("movie_id"))
        assert service_id >= 0 and movie_id > 0
    except (TypeError, AssertionError):
        return Response("Bad service ID and/or movie ID", 400)
    with Connection() as c:
        c.execute("INSERT INTO reservations(movie_id, service_id, user_id) VALUES (?,?,?)", (movie_id, service_id, user_id))
    return Response("Success", 201)


@app.route("/delete/<int:reservation_id>", methods=["POST"])
@login_required
def delete_reservation(reservation_id, user_id):
    with Connection() as c:
        rows = c.execute("SELECT * FROM reservations WHERE user_id = ? AND id = ?", (user_id, reservation_id)).fetchall()
        if rows:
            c.execute("DELETE FROM reservations WHERE id = ?", (reservation_id, ))
            return Response("Success", 200)
    return Response("Reservation not found", 404)


if __name__ == '__main__':
    app.run()
