import pathlib
from repositories.models import ArchivePaiement
from tools import JsonStorage

class ArchivePaiementRepo():

    PATH_ARCHIVE_PAIEMENT_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "archive_paiement.json"
    archive_paiement_json : list[ArchivePaiement] = JsonStorage.load_all(PATH_ARCHIVE_PAIEMENT_JSON)

    def __init__(self):
        """
        Initializes the ArchivePaiementRepo instance and loads all archive paiement data from the JSON file.
        If the JSON file does not exist, it initializes an empty list for archive paiement data.
        """
    def _save_all(self):
        JsonStorage.save_all(self.PATH_ARCHIVE_PAIEMENT_JSON, self.archive_paiement_json)

    def add_archive_paiement(self, archive_paiement : ArchivePaiement):
        if archive_paiement:
            self.archive_paiement_json.append(archive_paiement)
            self._save_all()
            return True
        return False 

    def delete_archive_paiement(self, archive_paiement : ArchivePaiement):
        if isinstance(archive_paiement, ArchivePaiement):
            self.archive_paiement_json.remove(archive_paiement)
            self._save_all()
            return True
        return False
        