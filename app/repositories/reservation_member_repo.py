import pathlib
from repositories.models import ReservationMember
from tools import JsonStorage

class ReservationMemberRepo:
    PATH_RESERVATION_MEMBER_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "reservation_member.json"
    def __init__(self):
        self._reservation_member_json : list[ReservationMember] = JsonStorage.load_all(self.PATH_RESERVATION_MEMBER_JSON)

    def _save_all(self):
        JsonStorage.save_all(self.PATH_RESERVATION_MEMBER_JSON, self._reservation_member_json)
    
    def add_reservation_member(self,id_member:int,id_reservation:int):
        self._reservation_member_json.append(ReservationMember(id_member=id_member, id_reservation=id_reservation))
        self._save_all()
    def update_reservation_member(self,id_member:int,id_reservation:int):
        for i,exist_res in enumerate(self._reservation_member_json):
            if exist_res.id == id_member:
                self._save_all()

    def get_reservation_member(self,id_member:int,id_reservation:int):
        pass

    def delete_reservation_member(self,id_member:int,id_reservation:int):
        pass 