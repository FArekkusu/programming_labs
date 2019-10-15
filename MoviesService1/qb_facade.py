from tables import Movies


class QBFacade:
    @classmethod
    def list_movies(cls, condition):
        query = Movies.objects.action("select").filters(condition).finalize()
        return [{
            "name": row["name"],
            "description": row["description"],
            "price": row["price"]
        } for row in query.execute()]
