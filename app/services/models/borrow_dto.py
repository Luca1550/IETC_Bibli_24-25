from repositories.models import Member
from datetime import date,datetime
from enums import PaymentType


class BorrowDTO:
    """
    Data Transfer Object for Borrow.
    This class is used to transfer borrow data between different layers of the application.
    """
    
    def __init__( self, id_borrow:int, id_exemplar:int, member:Member, borrow_date:date, return_date:date):
        """
        Initializes a BorrowDTO instance with the provided parameters.
        :param id_borrow: Unique identifier for the borrow record.
        :param id_exemplar: Unique identifier for the book exemplar being borrowed.
        :param member: Member who is borrowing the book.
        :param borrow_date: Date when the book was borrowed.
        :param return_date: Date when the book is expected to be returned.
        :param paiement_due: Amount due for the borrow.
        :param paiement_type: Type of payment for the borrow (e.g., cash, card).
        :param paiement_status: Status of the payment (e.g., paid, unpaid).
        """
        self.id_borrow = id_borrow
        self.id_exemplar = id_exemplar
        self.member = member
        self.borrow_date = borrow_date
        self.return_date = return_date
