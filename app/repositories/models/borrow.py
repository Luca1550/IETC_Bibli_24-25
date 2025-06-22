from datetime import datetime,date
from repositories.models import Base
from enums import PaiementType

class Borrow(Base):
    """Class representing a borrow record in the library system.
    This class inherits from Base and includes attributes such as
    id, id_exemplar, borrow_date, return_date, paiement_due, paiement_type, and paiement_status."""
    def __init__(self, id:int,id_exemplar:int, borrow_date:date, return_date:date):
        super().__init__(id)
        self.id_exemplar = id_exemplar
        self.borrow_date = borrow_date
        self.return_date = return_date