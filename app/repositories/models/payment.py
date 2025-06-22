from .base import Base
from enums import PaymentType
from datetime import date
class Payment (Base):
    """Class representing a payment record in the library system.
    This class inherits from Base and includes attributes such as payment type, amount due, and payment date."""
    def __init__(self, id:int |None,payment_type:int,payment_due:float, payment_date:date):
        """Initialize a payment instance with the given parameters.
        Args:
            id (int | None): The unique identifier for the payment record.
            payment_type (int): The type of payment, represented as an integer.
            payment_due (float): The amount due for the payment.
            payment_date (date): The date when the payment is due.
        """
        super().__init__(id)
        self.payment_type = payment_type
        self.payment_due = payment_due
        self.payment_date = payment_date
