from repositories.models import Member
from datetime import date

class PaiementDTO:
    """Class representing a payment record in the library system.
    This class includes attributes such as id_paiement, member, paiement_type, paiement_due"""
    def __init__(self, id_paiement: int | None, member:Member, paiement_type: int,paiement_due:int,paiement_date:date):
        """Class representing a payment record in the library system.
        This class includes attributes such as id_paiement, member, paiement_type, paiement_due, and paiement_date.
        """ 
        self.id_paiement = id_paiement
        self.member= member
        self.paiement_type = paiement_type
        self.paiement_due = paiement_due
        self.paiement_date = paiement_date

