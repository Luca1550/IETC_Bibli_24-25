from app.repositories.member_repo import MemberRepo
from repositories.models import PaiementMember,Member
from repositories import PaiementRepo
from tools import JsonStorage
import pathlib

class PaiementMemberRepo:
    
    PATH_PAIEMENT_MEMBER_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "paiement_member.json"

    paiement_member_json : list[PaiementMember] = JsonStorage.load_all(PATH_PAIEMENT_MEMBER_JSON)
    def __init__(self):
    
        self._member_repo : MemberRepo = MemberRepo()

    def _save_all(self):
        
        JsonStorage.save_all(self.PATH_PAIEMENT_MEMBER_JSON, self.paiement_member_json)

    def add_paiement_member(self,id_member:int,id_paiement:int):
        
        self.paiement_member_json.append(PaiementMember(id_member, id_paiement))
        self._save_all()

    def get_all(self):

        return self.paiement_member_json

    def get_members_by_paiement(self,id_paiement:int):

        lst_member : list[Member] = []
        for paiement_member in self.paiement_member_json:
            if paiement_member.id_paiement == id_paiement:
                lst_member.append(self._member_repo.get_member_by_id(paiement_member.id_member))
        return lst_member

    def delete_paiement_member(self,id_member:int,id_paiement:int):
        
        for paiement_member in self.paiement_member_json:
            if paiement_member.id_member == id_member and paiement_member.id_paiement == id_paiement:
                self.paiement_member_json.remove(paiement_member)
        self._save_all()
        