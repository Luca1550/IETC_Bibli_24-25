from repositories.models import Base
from datetime import datetime

class Reservation():
    def __init__(self,id:int | None,id_exemplar:int, id_member:int, reservation_date:datetime):
        super.__init__(id)
        self.id_exemplar=id_exemplar
        self.id_member=id_member
        self.reservation_date=reservation_date