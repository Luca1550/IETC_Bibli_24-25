import pathlib
from repositories.models import ReservationMember, Member
from repositories import MemberRepo
from tools import JsonStorage

class ReservationMemberRepo:
    PATH_RESERVATION_MEMBER_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "reservation_member.json"
    _reservation_member_json : list[ReservationMember] = JsonStorage.load_all(PATH_RESERVATION_MEMBER_JSON)
    
    def __init__(self):
        self.member_repo : MemberRepo = MemberRepo()

    def _save_all(self):
        JsonStorage.save_all(self.PATH_RESERVATION_MEMBER_JSON, self._reservation_member_json)
    
    def add_reservation_member(self,reservation_member: ReservationMember):
    
        self._reservation_member_json.append(reservation_member)
        self._save_all()
        return True
    
    def update_reservation_member(self,id_member:int,id_reservation:int):
        for exist_res in self._reservation_member_json:
            if exist_res.id_reservation == id_reservation:
                exist_res.id_member = id_member
                self._save_all()
                return True
        return False

    def get_reservation_member(self,id_member:int):
        result : list[ReservationMember] = []
        for reservation in self._reservation_member_json:
            if reservation.id_member == id_member:
                result.append(reservation)
        return result
        
    def get_reservation_member_byId(self, id_reservation: int):
        for reservation_member in self._reservation_member_json:
            if reservation_member.id_reservation == id_reservation:
                return self.member_repo.get_member_by_id(reservation_member.id_member)
        return None
    
    def delete_reservation_member(self,id_member:int,id_reservation:int):
        for things in self._reservation_member_json:
            if things.id_reservation == id_reservation and things.id_member == id_member:
                self._reservation_member_json.remove(things)
                self._save_all()
                return True
        return False
    