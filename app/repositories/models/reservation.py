from repositories.models import Base
from datetime import datetime

class Reservation():
    def __init__(self,id:int | None,id_exemplar:int, id_member:int, reservation_date:datetime):
        """
        Initializes a new reservation instance with a unique ID, exemplar ID, member ID and reservation date.
        If an ID is provided, it will be used; otherwise, a new unique ID is generated.

        Args:
            id (int | None): Unique identifier for the reservation. If None, a new ID is generated.
            id_exemplar (int): Unique identifier for the associated exemplar.
            id_member (int): Unique identifier for the associated member.
            reservation_date (datetime): Date of the reservation.
        """
        super.__init__(id)
        self.id_exemplar=id_exemplar
        self.id_member=id_member
        self.reservation_date=reservation_date