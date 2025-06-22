from repositories.models import Member
from datetime import date

class PaymentDTO:
    """Class representing a payment record in the library system.
    This class includes attributes such as id_payment, member, payment_type, payment_due"""
    def __init__(self, id_payment: int | None, member:Member, payment_type: int,payment_due:int,payment_date:date):
        """Class representing a payment record in the library system.
        This class includes attributes such as id_payment, member, payment_type, payment_due, and payment_date.
        """ 
        self.id_payment = id_payment
        self.member= member
        self.payment_type = payment_type
        self.payment_due = payment_due
        self.payment_date = payment_date

