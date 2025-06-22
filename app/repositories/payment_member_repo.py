from repositories.models import PaymentMember,Member
from repositories import PaymentRepo,MemberRepo
from tools import JsonStorage
import pathlib

class PaymentMemberRepo:
    """Repository for managing payment members in the library system.
    This class handles the storage and retrieval of payment member records."""
    PATH_PAYMENT_MEMBER_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "payment_member.json"

    payment_member_json : list[PaymentMember] = JsonStorage.load_all(PATH_PAYMENT_MEMBER_JSON)
    def __init__(self):
        """Initializes the PaymentMemberRepo instance and loads all payment member data from the JSON file.
        If the JSON file does not exist, it initializes an empty list for payment member data."""
        self._member_repo : MemberRepo = MemberRepo()

    def _save_all(self):
        """Saves all payment member data to the JSON file.
        This method is called after any modification to the payment member data to ensure that changes are persisted"""
        JsonStorage.save_all(self.PATH_PAYMENT_MEMBER_JSON, self.payment_member_json)

    def add_payment_member(self,paymentmember:PaymentMember):
        """Adds a PaymentMember object to the repository and saves it to the JSON file.
        arguments:
        - paymentmember: PaymentMember object to be added."""
        self.payment_member_json.append(paymentmember)
        self._save_all()

    def get_all(self):
        """Retrieves all PaymentMember objects from the repository.
        returns: A list of all PaymentMember objects.
        """
        return self.payment_member_json

    def get_members_by_payment(self,id_payment:int):
        """Retrieves all members associated with a specific payment ID.
        arguments:
        - id_payment: ID of the payment to retrieve associated members for.
        returns: A list of Member objects associated with the specified payment ID.
        """
        lst_member : list[Member] = []
        for payment_member in self.payment_member_json:
            if payment_member.id_payment == id_payment:
                lst_member.append(self._member_repo.get_member_by_id(payment_member.id_member))
        return lst_member

    def delete_payment_member(self,id_member:int,id_payment:int):
        """Deletes a paymentMember object from the repository based on member ID and payment ID.
        """
        for payment_member in self.payment_member_json:
            if payment_member.id_member == id_member and payment_member.id_payment == id_payment:
                self.payment_member_json.remove(payment_member)
        self._save_all()
        