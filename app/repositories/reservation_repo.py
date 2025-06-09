import pathlib
from repositories.models import Reservation
from tools import JsonStorage

class ReservationRepo():
    PATH_RESERVATION_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "reservation.json"

    def __init__(self):
        self.reservation_json : list[Reservation] = JsonStorage.load_all(self.PATH_RESERVATION_JSON)
    def add_reservation(self, reservation : Reservation):
        if reservation:
            self.reservation_json.append(reservation)
            self._save_all()
            return True
        return False 


    def get_reservation_parameters(self):
        return self.reservation_json

    def update_reservation(self, reservation : Reservation):
        for i, reserv in enumerate(self.reservation_json):
            if isinstance(reserv, dict):
                    if reserv.get('id') == reservation.id:
                        self.reservation_json[i] = reservation.__dict__  
                        self._save_all()
                        return True
        return False

    def delete_reservation(self, reservation : Reservation):
        pass

    def _save_all(self):
        JsonStorage.save_all(self.PATH_RESERVATION_JSON, self.reservation_json)  