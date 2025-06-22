from repositories.models import Base
from .member import Member
from datetime import date

class ArchivePayment(Base):
    """ Class representing an archived payment record in the library system.
    This class inherits from Base and includes attributes such as payment ID, member information, payment type, amount due, and payment date.
    """
    def __init__(self, id : int | None, id_payment:int, member:Member,payment_type:int,payment_due:float,payment_date:date):
        """Initialize an Archivepayment instance with the given parameters.
        Args:
            id (int | None): The unique identifier for the archived payment record.
            id_payment (int): The unique identifier for the payment.
            member (Member): The member associated with the payment.
            payment_type (int): The type of payment, represented as an integer.
            payment_due (float): The amount due for the payment.
            payment_date (date): The date when the payment is due.
        """
    
        super().__init__(id)
        self.id_payment = id_payment
        self.member= member
        self.payment_type = payment_type
        self.payment_due = payment_due
        self.payment_date = payment_date

