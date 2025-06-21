from repositories.models import Base
from .member import Member
from datetime import date

class ArchiveReservation(Base):

    def __init__(self, id : int | None, id_reservation:int, id_exemplar:int,member:Member,reservation_date:date):

    
        super().__init__(id)
        self.id_reservation = id_reservation
        self.id_exemplar = id_exemplar
        self.member = member
        self.reservation_date=reservation_date