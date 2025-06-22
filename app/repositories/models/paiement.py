from .base import Base
from enums import PaiementType
from datetime import date
class Paiement (Base):
    """Class representing a payment record in the library system.
    This class inherits from Base and includes attributes such as payment type, amount due, and payment date."""
    def __init__(self, id:int |None,paiement_type:int,paiement_due:float, paiement_date:date):
        """Initialize a Paiement instance with the given parameters.
        Args:
            id (int | None): The unique identifier for the payment record.
            paiement_type (int): The type of payment, represented as an integer.
            paiement_due (float): The amount due for the payment.
            paiement_date (date): The date when the payment is due.
        """
        super().__init__(id)
        self.paiement_type = paiement_type
        self.paiement_due = paiement_due
        self.paiement_date = paiement_date
