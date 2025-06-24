import pathlib
from repositories.models import ArchiveReservation
from tools import JsonStorage

class ArchiveReservationRepo():
    """
    Repository for managing Reservation objects.
    """
    PATH_ARCHIVE_RESERVATION_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "archive_reservation.json"
    archive_reservation_json : list[ArchiveReservation] = JsonStorage.load_all(PATH_ARCHIVE_RESERVATION_JSON)

    def __init__(self):
        """
        Initializes the ReservationRepo instance and loads all reservation data from the JSON file.
        If the JSON file does not exist, it initializes an empty list for reservation data.
        """
    def _save_all(self):
        JsonStorage.save_all(self.PATH_ARCHIVE_RESERVATION_JSON, self.archive_reservation_json)

    def add_archive_reservation(self, archive_reservation : ArchiveReservation):
        if archive_reservation:
            self.archive_reservation_json.append(archive_reservation)
            self._save_all()
            return True
        return False 

    def delete_archive_reservation(self, archive_reservation : ArchiveReservation):
        if isinstance(archive_reservation, ArchiveReservation):
            self.archive_reservation_json.remove(archive_reservation)
            self._save_all()
            return True
        return False
        