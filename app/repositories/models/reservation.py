from repositories.models import Base
from datetime import datetime

class Reservation(Base):
    def __init__(self,id:int | None,id_exemplar:int, reservation_date:datetime):
      
        super.__init__(id)
        self.id_exemplar=id_exemplar
        self.reservation_date=reservation_date