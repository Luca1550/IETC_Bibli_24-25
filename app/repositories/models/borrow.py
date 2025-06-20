import datetime 
from repositories.models import Base

class Borrow:
    """Class representing a borrow record in the library system.
    This class inherits from Base and includes attributes such as
    id, id_exemplar, borrow_date, return_date, paiement_due, paiement_type, and paiement_status."""
    def __init__(self, id:int,id_exemplar:int, borrow_date:datetime.date, return_date:datetime.date,paiement_due:float,paiement_type:str,paiement_status:bool):
       
       
        super().__init__(id)
        self.id_exemplar = id_exemplar
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.paiement_due = paiement_due
        self.paiement_type = paiement_type
        self.paiement_status = paiement_status