import pathlib
from repositories.models import Paiement
from tools import JsonStorage

class PaiementRepo:
    """Repository for managing Paiement objects, providing methods to add, update, delete, and retrieve paiement data.
    This class handles the storage and retrieval of paiement records in the library system."""
    PATH_PAIEMENT_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "paiement.json"

    _paiement_json : list[Paiement] = JsonStorage.load_all(PATH_PAIEMENT_JSON)
    def __init__(self):
       """Initializes the PaiementRepo instance and loads all paiement data from the JSON file."""
        
    def _save_all(self):
        """Saves all paiement data to the JSON file.
        This method is called after any modification to the paiement data to ensure that changes are persisted."""
        JsonStorage.save_all(self.PATH_PAIEMENT_JSON, self._paiement_json)

    def add_paiement(self, paiement : Paiement) :
        """Adds a Paiement object to the repository and saves it to the JSON file.
        arguments:
        - paiement: Paiement object to be added."""
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
    
    def get_paiement_parameters(self):
        """ Retrieves all Paiement objects from the repository.
        returns: A list of all Paiement objects.
        """
        return self._paiement_json

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
        """
        if isinstance(paiement, Paiement):
            self._paiement_json.remove(paiement)
            self._save_all()
            return True
        return False
    