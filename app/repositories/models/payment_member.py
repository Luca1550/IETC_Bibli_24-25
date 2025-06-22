class PaymentMember:
    """Model representing the association between a payment and a member in the library system."""
    def __init__(self,id_payment:int,id_member:int):
        """Initialize a paymentMember instance with the given parameters.
        Args:
            id_payment (int): The unique identifier for the payment record.
            id_member (int): The unique identifier for the member associated with the payment.
        """
        self.id_payment = id_payment
        self.id_member = id_member