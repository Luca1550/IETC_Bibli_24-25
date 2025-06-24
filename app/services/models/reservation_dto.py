from repositories.models import Member
from datetime import date

class ReservationDTO:
    """
    Data Transfer Object for Reservation.
    This class is used to transfer reservation data between different layers of the application.
    """
    def __init__(self,id_reservation:int, id_exemplar:int,member:Member,reservation_date:date ):
        self.id_reservation = id_reservation
        self.id_exemplar = id_exemplar
        self.member = member
        self.reservation_date=reservation_date
