from .base import Base
from enums import PaiementType
from datetime import date
class Paiement (Base):
    def __init__(self, id:int |None,paiement_type:int,paiement_due:int, paiement_date:date):
        super().__init__(id)
        self.paiement_type = paiement_type
        self.paiement_due = paiement_due
        self.paiement_date = paiement_date
