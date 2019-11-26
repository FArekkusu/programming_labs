from tables import Movies


class QBFacade:
    @classmethod
    def list_movies(cls, condition):
        query = Movies.objects.action("select").filters(condition).finalize()
        return query.execute()
