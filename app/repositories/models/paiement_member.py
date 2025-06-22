class PaiementMember:
    """Model representing the association between a payment and a member in the library system."""
    def __init__(self,id_paiement:int,id_member:int):
        """Initialize a PaiementMember instance with the given parameters.
        Args:
            id_paiement (int): The unique identifier for the payment record.
            id_member (int): The unique identifier for the member associated with the payment.
        """
        self.id_paiement = id_paiement
        self.id_member = id_member