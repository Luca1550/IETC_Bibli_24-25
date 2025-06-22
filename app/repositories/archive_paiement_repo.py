import pathlib
from repositories.models import ArchivePaiement
from tools import JsonStorage

class ArchivePaiementRepo():
    """Repository for managing ArchivePaiement objects.
    This class handles the storage and retrieval of archive paiement records in the library system."""
    PATH_ARCHIVE_PAIEMENT_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "archive_paiement.json"
    archive_paiement_json : list[ArchivePaiement] = JsonStorage.load_all(PATH_ARCHIVE_PAIEMENT_JSON)

    def __init__(self):
        """Initializes the ArchivePaiementRepo instance and loads all archive paiement data from the JSON file."""
    def _save_all(self):
        """Saves all archive paiement data to the JSON file."""
        JsonStorage.save_all(self.PATH_ARCHIVE_PAIEMENT_JSON, self.archive_paiement_json)

    def add_archive_paiement(self, archive_paiement : ArchivePaiement):
        """Adds an ArchivePaiement object to the repository and saves it to the JSON file.
        arguments:
        - archive_paiement: ArchivePaiement object to be added.
        """
        if archive_paiement:
            self.archive_paiement_json.append(archive_paiement)
            self._save_all()
            return True
        return False 

    def delete_archive_paiement(self, archive_paiement : ArchivePaiement):
        """Deletes an ArchivePaiement object from the repository and saves the changes to the JSON file.
        arguments:
        - archive_paiement: ArchivePaiement object to be deleted.
        returns: True if the archive paiement was deleted successfully, otherwise returns False.
        """
        if isinstance(archive_paiement, ArchivePaiement):
            self.archive_paiement_json.remove(archive_paiement)
            self._save_all()
            return True
        return False
        