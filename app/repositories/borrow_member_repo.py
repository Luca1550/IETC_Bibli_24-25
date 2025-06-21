from repositories.models import BorrowMember, Member
from repositories import MemberRepo
from tools import JsonStorage
import pathlib
class BorrowMemberRepo:
    """
    Repository for managing BorrowMember objects.
    This class handles the storage and retrieval of borrow records associated with members.
    """
    PATH_BORROW_MEMBER_JSON = pathlib.Path(__file__).parent.parent.parent / "database" / "borrow_member.json"
    _borrow_member_json: list[BorrowMember] = JsonStorage.load_all(PATH_BORROW_MEMBER_JSON)

    def __init__(self):
        self.member_repo: MemberRepo = MemberRepo()

    def _save_all(self):
        JsonStorage.save_all(self.PATH_BORROW_MEMBER_JSON, self._borrow_member_json)

    def add_borrow_member(self, borrow_member: BorrowMember) :
        """
        Adds a BorrowMember object to the repository and saves it to the JSON file.
        """
        if isinstance(borrow_member, BorrowMember):
            self._borrow_member_json.append(borrow_member)
            self._save_all()
            return True
        return False
    
    def get_borrow_by_member(self, id_member:int):
        result = []
        for member in self._borrow_member_json:
            if member.id_member == id_member:
                result.append(member)
        return result

    def get_borrow_members(self,id_member:int,id_borrow:int):
        Listmemb : list[Member] = []
        for truc in self._borrow_member_json:
            if truc.id_borrow == id_borrow:
                member = self.member_repo.get_member_by_id(truc.id_member)
                if member:
                    Listmemb.append(member)
        return Listmemb

    def update_borrow_member(self,id_member:int,id_borrow:int) :
        """
        Updates an existing BorrowMember object in the repository and saves the changes to the JSON file.
        """
        for exist_bor in self._borrow_member_json:
            if exist_bor.id_borrow == id_borrow:
                exist_bor.id_member = id_member
                self._save_all()
                return True
        return False

    def delete_borrow_member(self,id_member:int,id_borrow:int) :
        """
        Deletes a BorrowMember object from the repository and saves the changes to the JSON file.
        """
        for things in self._borrow_member_json:
            if things.id_borrow == id_borrow and things.id_member == id_member:
                self._borrow_member_json.remove(things)
                self._save_all()
                return True
        return False

    def get_borrow_member_by_id(self, id_borrow: int) :
    
        for borrow_member in self._borrow_member_json:
            if borrow_member.id_borrow == id_borrow:           
                return self.member_repo.get_member_by_id(borrow_member.id_member)
        return None