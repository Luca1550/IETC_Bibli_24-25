from repositories.models import Member
import datetime

class ReservationDTO:
    
    def __init__(self,id_reservation:int, id_exemplar:int,member:Member,reservation_date:datetime ):
        self.id_reservation = id_reservation
        self.id_exemplar = id_exemplar
        self.member = member
        self.reservation_date=reservation_date
