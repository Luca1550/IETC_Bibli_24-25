import pathlib
from repositories.models import ReservationMember, Member
from repositories import MemberRepo
from tools import JsonStorage

class ReservationMemberRepo:
    """
    Repository for managing ReservationMember objects.
    """
    PATH_RESERVATION_MEMBER_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "reservation_member.json"
    _reservation_member_json : list[ReservationMember] = JsonStorage.load_all(PATH_RESERVATION_MEMBER_JSON)
    
    def __init__(self):
        self.member_repo : MemberRepo = MemberRepo()

    def _save_all(self):
        JsonStorage.save_all(self.PATH_RESERVATION_MEMBER_JSON, self._reservation_member_json)
    
    def add_reservation_member(self,reservation_member: ReservationMember):
        """
        Adds a ReservationMember object to the repository and saves it to the JSON file.
        arguments:
        - reservation_member: ReservationMember object to be added.
        returns:
        - True if the reservation member was added successfully, False otherwise.
        """
        self._reservation_member_json.append(reservation_member)
        self._save_all()
        return True
    
    def update_reservation_member(self,id_member:int,id_reservation:int):
        """
        Updates an existing ReservationMember object in the repository and saves the changes to the JSON file.
        arguments:
        - id_member: ID of the member to update.
        - id_reservation: ID of the reservation to update.
        returns:
        - True if the reservation member was updated successfully, otherwise returns False.
        """
        for exist_res in self._reservation_member_json:
            if exist_res.id_reservation == id_reservation:
                exist_res.id_member = id_member
                self._save_all()
                return True
        return False

    def get_reservation_member(self,id_member:int):
        """
        Retrieves all ReservationMember objects associated with a specific member ID.
        arguments:
        - id_member: ID of the member whose reservations are to be retrieved.
        returns:
        - A list of ReservationMember objects associated with the specified member ID.
        """
        result : list[ReservationMember] = []
        for reservation in self._reservation_member_json:
            if reservation.id_member == id_member:
                result.append(reservation)
        return result
        
    def get_reservation_member_byId(self, id_reservation: int):
        """
        Retrieves a ReservationMember object by its reservation ID.
        arguments:
        - id_reservation: ID of the reservation to retrieve.
        returns:
        - The ReservationMember object if found, otherwise returns None.
        """
        for reservation_member in self._reservation_member_json:
            if reservation_member.id_reservation == id_reservation:
                return self.member_repo.get_member_by_id(reservation_member.id_member)
        return None
    
    def delete_reservation_member(self,id_member:int,id_reservation:int):
        """
        Deletes a ReservationMember object from the repository and saves the changes to the JSON file.
        arguments:
        - id_member: ID of the member whose reservation is to be deleted.
        - id_reservation: ID of the reservation to be deleted.
        returns:
        - True if the reservation member was deleted successfully, otherwise returns False.
        """
        for things in self._reservation_member_json:
            if things.id_reservation == id_reservation and things.id_member == id_member:
                self._reservation_member_json.remove(things)
                self._save_all()
                return True
        return False
    