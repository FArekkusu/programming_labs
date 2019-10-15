from specification import Specification
from datetime import datetime
from operator import eq, lt, gt


def comparison_specification_factory(op):
    class Compare(Specification):
        def __init__(self, field, value, *, function=lambda x: x):
            self.field = field
            self.value = value
            self.function = function

        def check(self, row):
            return op(self.function(row[self.field]), self.value)

    return Compare


Equals = comparison_specification_factory(eq)
Less = comparison_specification_factory(lt)
Greater = comparison_specification_factory(gt)


class Released(Specification):
    def check(self, row):
        return Less("release_date", datetime.today(), function=parse_date).check(row)


class Always(Specification):
    def check(self, row):
        return True


def parse_date(value):
    return datetime.strptime(value, "%d-%m-%Y")
