from repositories.models import Base
from .member import Member
from datetime import date

class ArchivePaiement(Base):

    def __init__(self, id : int | None, id_paiement:int, member:Member,paiement_type:int,paiement_due:float,paiement_date:date):

    
        super().__init__(id)
        self.id_paiement = id_paiement
        self.member= member
        self.paiement_type = paiement_type
        self.paiement_due = paiement_due
        self.paiement_date = paiement_date

