from .base import Base
from enums import PaiementType
class Paiement (Base):
    def __init__(self, id:int |None,paiement_type:int):
        super().__init__(id)
        paiement_type = PaiementType()
        statut=statut
