import pathlib
from repositories.models import Paiement
from tools import JsonStorage

class PaiementRepo:
    """
    Repository for managing Person objects.
    arguments:
    - PATH_PERSON_JSON: Path to the JSON file where Person data is stored.
    """
    PATH_PAIEMENT_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "paiement.json"

    _paiement_json : list[Paiement] = JsonStorage.load_all(PATH_PAIEMENT_JSON)
    def __init__(self):
        """
        Initializes the PaiementRepo instance and loads all Paiement data from the JSON file.
        If the JSON file does not exist, it initializes an empty list for Paiement data.
        """
        
    def _save_all(self):
        
        JsonStorage.save_all(self.PATH_PAIEMENT_JSON, self._paiement_json)

    def add_paiement(self, paiement : Paiement) -> bool:

        if isinstance(paiement, Paiement):
            self._paiement_json.append(paiement)
            self._save_all()
            return True
        return False
    
    def get_by_id(self, id : int):
        """
        Retrieves a Paiement object by its ID.
        arguments:
        - id: ID of the Paiement to retrieve.
        returns:
        - Returns the Paiement object if found, otherwise returns False.
        """
        if id:
            return next((p for p in self._paiement_json if p.id == id), None)
        return False

    def update_paiement(self, paiement : Paiement) -> bool:
        """
        Updates an existing Paiement object in the repository and saves the changes to the JSON file.
        arguments:
        - paiement: Paiement object to be updated.
        returns:
        - True if the paiement was updated successfully, otherwise returns False.
        """
        if isinstance(paiement, Paiement):
            self._paiement_json[self._paiement_json.index(paiement)] = paiement
            self._save_all()
            return True
        return False

    def delete_paiement(self, paiement : Paiement) -> bool:
        """
        Deletes a Paiement object from the repository and saves the changes to the JSON file.
        arguments:
        - paiement: Paiement object to be deleted.
        returns:
        - True if the paiement was deleted successfully, False otherwise.
        """
        if isinstance(paiement, Paiement):
            self._paiement_json.remove(paiement)
            self._save_all()
            return True
        return False
    