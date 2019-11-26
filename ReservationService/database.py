import sqlite3


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Connection(metaclass=Singleton):
    def __init__(self, db=None):
        self._db = sqlite3.connect(db, check_same_thread=False)

    def __enter__(self):
        return self._db.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.commit()


class Query:
    def __init__(self, table, action, filters, values):
        self.table = table
        self.action = action
        self.filters = filters
        self.values = values

    def execute(self):
        if self.action == "select":
            with Connection() as c:
                rows = c.execute(f"SELECT * FROM {self.table}")
                rows = add_column_headers(rows, c)
                if self.filters:
                    rows = [r for r in rows if self.filters.check(r)]
            return rows
        if self.action == "insert":
            with Connection() as c:
                q = ",".join("?" * len(self.values))
                query = f"INSERT INTO {self.table}({','.join(self.values.keys())}) VALUES ({q})"
                c.execute(query, [*self.values.values()])
                return True
        elif self.action == "delete":
            with Connection() as c:
                rows = c.execute(f"SELECT * FROM {self.table}")
                rows = add_column_headers(rows, c)
                rows = [r["id"] for r in rows if self.filters.check(r)]
                q = ",".join("?" * len(rows))
                c.execute(f"DELETE FROM {self.table} WHERE id IN ({q})", rows)
                return True


class QueryBuilder:
    def __init__(self):
        self._table = None
        self._action = None
        self._filters = None
        self._values = None

    def table(self, table):
        self._table = table
        return self

    def action(self, action):
        self._action = action
        return self

    def filters(self, filters):
        self._filters = filters
        return self

    def values(self, values):
        self._values = values
        return self

    def finalize(self):
        return Query(self._table, self._action, self._filters, self._values)


def add_column_headers(rows, conn):
    columns = [x[0] for x in conn.description]
    return [{c: v for c, v in zip(columns, row)} for row in rows]
