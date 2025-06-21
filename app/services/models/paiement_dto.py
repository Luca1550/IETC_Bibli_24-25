from repositories.models import Member
from datetime import date

class PaiementDTO:
    def __init__(self, id_paiement: int | None, member:Member, paiement_type: int, date_paiement: date):
    
        self.id_paiement = id_paiement
        self.member= member
        self.paiement_type = paiement_type
        self.date_paiement = date_paiement
