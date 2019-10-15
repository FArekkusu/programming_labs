from database import QueryBuilder


class TableMeta(type):
    @property
    def objects(cls):
        return QueryBuilder().table(cls._name)


def table_factory(name):
    class Table(metaclass=TableMeta):
        _name = name

    return Table


Movies = table_factory("movies")
