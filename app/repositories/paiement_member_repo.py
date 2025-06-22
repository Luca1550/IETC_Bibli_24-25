from repositories.models import PaiementMember,Member
from repositories import PaiementRepo,MemberRepo
from tools import JsonStorage
import pathlib

class PaiementMemberRepo:
    """Repository for managing payment members in the library system.
    This class handles the storage and retrieval of payment member records."""
    PATH_PAIEMENT_MEMBER_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "paiement_member.json"

    paiement_member_json : list[PaiementMember] = JsonStorage.load_all(PATH_PAIEMENT_MEMBER_JSON)
    def __init__(self):
        """Initializes the PaiementMemberRepo instance and loads all payment member data from the JSON file.
        If the JSON file does not exist, it initializes an empty list for payment member data."""
        self._member_repo : MemberRepo = MemberRepo()

    def _save_all(self):
        """Saves all payment member data to the JSON file.
        This method is called after any modification to the payment member data to ensure that changes are persisted"""
        JsonStorage.save_all(self.PATH_PAIEMENT_MEMBER_JSON, self.paiement_member_json)

    def add_paiement_member(self,paiementmember:PaiementMember):
        """Adds a PaiementMember object to the repository and saves it to the JSON file.
        arguments:
        - paiementmember: PaiementMember object to be added."""
        self.paiement_member_json.append(paiementmember)
        self._save_all()

    def get_all(self):
        """Retrieves all PaiementMember objects from the repository.
        returns: A list of all PaiementMember objects.
        """
        return self.paiement_member_json

    def get_members_by_paiement(self,id_paiement:int):
        """Retrieves all members associated with a specific payment ID.
        arguments:
        - id_paiement: ID of the payment to retrieve associated members for.
        returns: A list of Member objects associated with the specified payment ID.
        """
        lst_member : list[Member] = []
        for paiement_member in self.paiement_member_json:
            if paiement_member.id_paiement == id_paiement:
                lst_member.append(self._member_repo.get_member_by_id(paiement_member.id_member))
        return lst_member

    def delete_paiement_member(self,id_member:int,id_paiement:int):
        """Deletes a PaiementMember object from the repository based on member ID and payment ID.
        """
        for paiement_member in self.paiement_member_json:
            if paiement_member.id_member == id_member and paiement_member.id_paiement == id_paiement:
                self.paiement_member_json.remove(paiement_member)
        self._save_all()
        