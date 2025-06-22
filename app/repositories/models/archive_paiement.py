from repositories.models import Base
from .member import Member
from datetime import date

class ArchivePaiement(Base):
    """ Class representing an archived payment record in the library system.
    This class inherits from Base and includes attributes such as payment ID, member information, payment type, amount due, and payment date.
    """
    def __init__(self, id : int | None, id_paiement:int, member:Member,paiement_type:int,paiement_due:float,paiement_date:date):
        """Initialize an ArchivePaiement instance with the given parameters.
        Args:
            id (int | None): The unique identifier for the archived payment record.
            id_paiement (int): The unique identifier for the payment.
            member (Member): The member associated with the payment.
            paiement_type (int): The type of payment, represented as an integer.
            paiement_due (float): The amount due for the payment.
            paiement_date (date): The date when the payment is due.
        """
    
        super().__init__(id)
        self.id_paiement = id_paiement
        self.member= member
        self.paiement_type = paiement_type
        self.paiement_due = paiement_due
        self.paiement_date = paiement_date

