from tables import Movies


class QBFacade:
    @classmethod
    def list_movies(cls):
        query = Movies.objects.action("select").finalize()
        return sorted(query.execute(), key=lambda x: x["id"])

    @classmethod
    def get_movie(cls, condition):
        query = Movies.objects.action("select").filters(condition).finalize()
        result = query.execute()
        if result:
            return result[0]
