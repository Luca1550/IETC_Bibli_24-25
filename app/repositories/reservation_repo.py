import pathlib
from repositories.models import Reservation
from tools import JsonStorage

class ReservationRepo():
    """
    Repository for managing Reservation objects."""
    PATH_RESERVATION_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "reservation.json"
    reservation_json : list[Reservation] = JsonStorage.load_all(PATH_RESERVATION_JSON)

    def __init__(self):
        """
        Initializes the ReservationRepo instance and loads all reservation data from the JSON file.
        If the JSON file does not exist, it initializes an empty list for reservation data.
        """
        
    def add_reservation(self, reservation : Reservation):
        """ Adds a Reservation object to the repository and saves it to the JSON file.
        arguments:
        - reservation: Reservation object to be added.
        returns:
        - True if the reservation was added successfully, False otherwise.
        """
        if reservation:
            self.reservation_json.append(reservation)
            self._save_all()
            return True
        return False 

    def get_by_id(self,id):
        """ Retrieves a Reservation object by its ID.
        arguments:
        - id: ID of the Reservation to retrieve.
        returns:
        - Returns the Reservation object if found, otherwise returns None."""
        for reservation in self.reservation_json:
            if reservation.id == id:
                return reservation
        return None
    def get_reservation_parameters(self):
        """ Retrieves reservation parameters from the repository.
        Returns a list of reservation parameters."""
        return self.reservation_json

    def update_reservation(self, reservation : Reservation):
        """ Updates an existing Reservation object in the repository and saves the changes to the JSON file.
        arguments:
        - reservation: Reservation object to be updated.
        returns:
        - True if the reservation was updated successfully, otherwise returns False.
        """
        for i, reserv in enumerate(self.reservation_json):
            if isinstance(reserv, Reservation):
                    if reserv.id == reservation.id:
                        self.reservation_json[i] = reservation
                        self._save_all()
                        return True
        return False

    def delete_reservation(self, reservation : Reservation):
        """ Deletes a Reservation object from the repository and saves the changes to the JSON file.
        arguments:
        - reservation: Reservation object to be deleted.
        returns:
        - True if the reservation was deleted successfully, otherwise returns False.
        """
        if isinstance(reservation, Reservation):
            self.reservation_json.remove(reservation)
            self._save_all()
            return True
        return False
    
    def check(self, attribute: str, value: object) -> bool:
        """
        Checks whether a given attribute with the specified value exists in the repository.

        Arguments:
        - attribute: The name of the attribute to check.
        - value: The value to look for in that attribute.

        Returns:
        - True if any object in the repository has the given value for the attribute; False otherwise.
        """
        return any(getattr(reservation, attribute, None) == value for reservation in self.reservation_json)

        
    def _save_all(self):
        """ Saves all Reservation data to the JSON file."""
        JsonStorage.save_all(self.PATH_RESERVATION_JSON, self.reservation_json)  