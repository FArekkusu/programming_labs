from graphene import Schema, ObjectType, Mutation, String, Int, Boolean, Field, List
import requests
from database import Connection


class Movie(ObjectType):
    id = Int()
    name = String()
    description = String()
    price = Int()
    service = Int()


class User(ObjectType):
    id = Int()
    login = String()
    password = String()
    last_auth = String()


class Reservation(ObjectType):
    id = Int()
    service_id = Int()
    movie_id = Int()


class Query(ObjectType):
    movies = List(Movie, id=Int(), name=String(), price=Int(), service=Int())
    users = List(User, id=Int(), login=String())
    reservations = List(Reservation, token=String(required=True))

    @staticmethod
    def resolve_movies(root, info, **kwargs):
        from app import get_all_movies
        return apply_filters(get_all_movies(), kwargs)

    @staticmethod
    def resolve_users(root, info, **kwargs):
        return apply_filters(requests.get("http://127.0.0.1:5004/list_users").json(), kwargs)

    @staticmethod
    def resolve_reservations(root, info, token):
        return requests.post("http://127.0.0.1:5003/list", data={"token": token}).json()


class CreateReservation(Mutation):
    class Arguments:
        token = String()
        service_id = Int()
        movie_id = Int()

    ok = Boolean()
    reservation = Field(Reservation)

    @staticmethod
    def mutate(root, info, token, service_id, movie_id):
        result = requests.post("http://127.0.0.1:5003/create",
                               data={"token": token, "service_id": service_id, "movie_id": movie_id}).json()
        return CreateReservation(reservation=Reservation(result, service_id, movie_id), ok=True)


class CreateMovie(Mutation):
    class Arguments:
        name = String()
        runtime = Int()
        description = String()
        price = Int()
        release_date = String()

    ok = Boolean()
    movie = Field(Movie)

    @staticmethod
    def mutate(root, info, name, runtime, description, price, release_date):
        with Connection() as c:
            c.execute("INSERT INTO movies(name, runtime, description, price, release_date) VALUES (?, ?, ?, ?, ?)",
                      (name, runtime, description, price, release_date))
            last_row_id = c.lastrowid
        return CreateMovie(movie=Movie(last_row_id, name, description, price, 0), ok=True)


class EditMovie(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        description = String()
        price = Int()

    ok = Boolean()
    movie = Field(Movie)

    @staticmethod
    def mutate(root, info, id, **kwargs):
        if kwargs:
            keys = ", ".join(f"{x} = ?" for x in kwargs.keys())
            values = tuple(kwargs.values()) + (id, )
            with Connection() as c:
                c.execute(f"UPDATE movies SET {keys} WHERE id = ?", values)
        with Connection() as c:
            name, description, price = c.execute("SELECT name, description, price FROM movies WHERE id = ?", (id, )).fetchone()
        return EditMovie(movie=Movie(id, name, description, price, 0), ok=True)


class DeleteMovie(Mutation):
    class Arguments:
        id = Int()

    ok = Boolean()

    @staticmethod
    def mutate(root, info, id):
        with Connection() as c:
            c.execute("DELETE FROM movies WHERE id = ?", (id, ))
        return DeleteMovie(ok=True)


class MyMutation(ObjectType):
    create_reservation = CreateReservation.Field()
    create_movie = CreateMovie.Field()
    edit_movie = EditMovie.Field()
    delete_movie = DeleteMovie.Field()


def apply_filters(rows, filters):
    for k, v in filters.items():
        rows = [row for row in rows if row[k] == v]
    return rows


schema = Schema(query=Query, mutation=MyMutation)
