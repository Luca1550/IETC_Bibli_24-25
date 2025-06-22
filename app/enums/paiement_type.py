from enum import Enum

class PaiementType(Enum):
    """Enum representing different types of payments in the library system."""
    FINE=1
    LOST_BOOK=2
    BORROW_WITH_SUB=3
    BORROW_WITHOUT_SUB=4
