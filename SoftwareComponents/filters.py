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


class Started(Specification):
    def check(self, row):
        field = "start_time"
        today = datetime.today()
        return (Less(field, today, function=parse_date) | Equals(field, today, function=parse_date)).check(row)


class Finished(Specification):
    def check(self, row):
        return Less("end_time", datetime.today(), function=parse_date).check(row)


class Paid(Specification):
    def check(self, row):
        return Equals("paid", True).check(row)


class AwaitingPayment(Specification):
    def check(self, row):
        return (~Paid()).check(row)


class Always(Specification):
    def check(self, row):
        return True


def parse_date(value):
    return datetime.strptime(value, "%d-%m-%Y")
