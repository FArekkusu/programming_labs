import re
import threading
from datetime import datetime, timedelta
from time import sleep
from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_graphql import GraphQLView
from services import make_requests_to_services, FETCH_HANDLERS
from filters import Always, Greater, Less, Equals, parse_date, normalize_string
from qb_facade import QBFacade
from graphene_setup import schema


app = Flask(__name__)
app.config.from_mapping({"DEBUG": True, "CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 60 * 60 * 25})
cache = Cache(app)
next_update_at = datetime.now()
update_in_process = False

app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True, context=cache))


def update_cache():
    global next_update_at
    global update_in_process

    while 1:
        if not update_in_process and datetime.now() >= next_update_at:
            update_in_process = True
            next_update_at = datetime.now() + timedelta(hours=2)
            print(f"START AT {datetime.now().strftime('%H:%M:%S')}")
            make_requests_to_services(cache)
            print(f"END AT {datetime.now().strftime('%H:%M:%S')}")
            print(f"NEXT UPDATE AT {next_update_at}")
            update_in_process = False
        else:
            sleep(60)


cache_updater = threading.Thread(target=update_cache, daemon=True)
cache_updater.start()


def get_all_movies():
    movies = QBFacade.list_movies(Always())
    for row in movies:
        row["service"] = 0
    movies.sort(key=lambda x: x["name"])
    for (_, key) in FETCH_HANDLERS:
        movies.extend(cache.get(key) or [])
    return movies

@app.route("/")
def home():
    return "Running"


@app.route("/movies", methods=["GET"])
def list_movies():
    condition = Always()
    for field, query in request.args.items():
        comparison, value = query[:2], query[4:]
        filter_condition = {"gt": Greater, "lt": Less, "eq": Equals}[comparison]
        function = parse_date if re.match(r"(\d\d-){2}\d{4}$", value) else int if re.match(r"\d+$", value) else normalize_string
        condition &= filter_condition(field, function(value), function=function)
    movies = get_all_movies()
    result = [{k: row[k] for k in "id name description price service".split()}
              for row in movies if condition.check(row)]
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
        c.executemany("INSERT INTO movies(name, price, runtime, description, release_date) VALUES (?,?,?,?,?)", rows)
    finish = T()
    return str(finish - start)


if __name__ == '__main__':
    app.run()
