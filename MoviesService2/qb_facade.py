from tables import Movies


class QBFacade:
    @classmethod
    def list_movies(cls):
        query = Movies.objects.action("select").finalize()
        return [{"name": row["name"], "price": row["price"]} for row in query.execute()]

    @classmethod
    def get_movie(cls, condition):
        query = Movies.objects.action("select").filters(condition).finalize()
        result = query.execute()
        if result:
            return result[0]
