from filters import AwaitingPayment
from tables import Reservations


class QBFacade:
    @classmethod
    def list_reservations(cls, condition):
        query = Reservations.objects.action("select").filters(condition).finalize()
        return query.execute()

    @classmethod
    def add_reservation(cls, values):
        query = Reservations.objects.action("insert").values(values).finalize()
        return query.execute()

    @classmethod
    def clear_non_paid_reservations(cls):
        query = Reservations.objects.action("delete").filters(AwaitingPayment()).finalize()
        return query.execute()
