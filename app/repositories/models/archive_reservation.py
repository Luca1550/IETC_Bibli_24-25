from repositories.models import Base
from .member import Member
from datetime import date

class ArchiveReservation(Base):
    """ Class representing an archived reservation record in the library system.
    This class inherits from Base and includes attributes such as reservation ID, exemplar ID, member information, and reservation date."""
    def __init__(self, id : int | None, id_reservation:int, id_exemplar:int,member:Member,reservation_date:date):
        """Initialize an ArchiveReservation instance with the given parameters.
        Args:
            id (int | None): The unique identifier for the archived reservation record.
            id_reservation (int): The unique identifier for the reservation.
            id_exemplar (int): The unique identifier for the exemplar associated with the reservation.
            member (Member): The member associated with the reservation.
            reservation_date (date): The date when the reservation was made.
        """
    
        super().__init__(id)
        self.id_reservation = id_reservation
        self.id_exemplar = id_exemplar
        self.member = member
        self.reservation_date=reservation_date