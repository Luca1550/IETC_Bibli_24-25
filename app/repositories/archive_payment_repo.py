import pathlib
from repositories.models import ArchivePayment
from tools import JsonStorage

class ArchivePaymentRepo():
    """
    Repository for managing ArchivePayment objects.
    This class handles the storage and retrieval of archive payment records in the library system.
    """
    PATH_ARCHIVE_PAYMENT_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "archive_payment.json"
    archive_payment_json : list[ArchivePayment] = JsonStorage.load_all(PATH_ARCHIVE_PAYMENT_JSON)

    def __init__(self):
        """Initializes the ArchivePaymentRepo instance and loads all archive payment data from the JSON file."""
    def _save_all(self):
        """Saves all archive payment data to the JSON file."""
        JsonStorage.save_all(self.PATH_ARCHIVE_PAYMENT_JSON, self.archive_payment_json)

    def add_archive_payment(self, archive_payment : ArchivePayment):
        """Adds an ArchivePayment object to the repository and saves it to the JSON file.
        arguments:
        - archive_payment: ArchivePayment object to be added.
        """
        if archive_payment:
            self.archive_payment_json.append(archive_payment)
            self._save_all()
            return True
        return False 

    def delete_archive_payment(self, archive_payment : ArchivePayment):
        """Deletes an ArchivePayment object from the repository and saves the changes to the JSON file.
        arguments:
        - archive_payment: ArchivePayment object to be deleted.
        returns: True if the archive payment was deleted successfully, otherwise returns False.
        """
        if isinstance(archive_payment, ArchivePayment):
            self.archive_payment_json.remove(archive_payment)
            self._save_all()
            return True
        return False
        