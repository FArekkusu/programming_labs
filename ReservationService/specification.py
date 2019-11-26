class Specification:
    def __init__(self, *args, **kwargs):
        pass

    def __and__(self, other):
        return AndSpecification(self, other)

    def __or__(self, other):
        return OrSpecification(self, other)

    def __invert__(self):
        return NotSpecification(self)


class AndSpecification(Specification):
    def __init__(self, spec_1, spec_2):
        self.spec_1 = spec_1
        self.spec_2 = spec_2

    def check(self, value):
        return self.spec_1.check(value) and self.spec_2.check(value)


class OrSpecification(Specification):
    def __init__(self, spec_1, spec_2):
        self.spec_1 = spec_1
        self.spec_2 = spec_2

    def check(self, value):
        return self.spec_1.check(value) or self.spec_2.check(value)


class NotSpecification(Specification):
    def __init__(self, spec):
        self.spec = spec

    def check(self, value):
        return not self.spec.check(value)

