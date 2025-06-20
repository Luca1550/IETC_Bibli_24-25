from .models import Exemplar
from tools import JsonStorage
from enums import Status
import pathlib

class ExemplarRepo():
    """
    Repository class for managing book exemplars.
    """
    PATH_EXEMPLAR_JSON = pathlib.Path(__file__).parent.parent.parent / "database" / "exemplar.json"

    _exemplar_json : list[Exemplar] = JsonStorage.load_all(PATH_EXEMPLAR_JSON)
    def __init__(self):
        """
        Initializes the ExemplarRepo and loads all exemplars from the JSON file.
        """
    
    def _save_all(self):
        """
        Saves all exemplars to the JSON file.
        """
        JsonStorage.save_all(self.PATH_EXEMPLAR_JSON, self._exemplar_json)

    def add_exemplar(self, exemplar : Exemplar):
        """
        Adds a new exemplar to the repository and saves it to the JSON file.
        Args:
            exemplar (Exemplar): The exemplar to be added.
        """
        if isinstance(exemplar, Exemplar):
            self._exemplar_json.append(exemplar)
            self._save_all()
            return True
        return False
    
    def get_by_id(self, id : int):
        """
        Retrieves a Exemplar object by its ID.
        arguments:
        - id: ID of the Exemplar to retrieve.
        returns:
        - Returns the Exemplar object if found, otherwise returns False.
        """
        if id:
            return next((e for e in self._exemplar_json if e.id == id), None)
        return False
    
    def get_all(self, isbn : str) -> list[Exemplar]:
        """
        Retrieves all Exemplar objects from the repository.
        returns:
        - Returns a list of all Exemplar objects.
        """
        exemplars = []
        for exemplar in self._exemplar_json:
            if exemplar.isbn == isbn:
                exemplars.append(exemplar)
        return exemplars

    def get_disponibility(self, isbn : str) -> Exemplar | bool:
        if isbn:
            return next((e for e in self._exemplar_json if e.isbn == isbn and e.status == Status(1)), None)
        return False
    
    def delete_exemplar(self, exemplar : Exemplar) -> bool:
        """
        Deletes an Exemplar object from the repository and saves the changes to the JSON file.
        arguments:
        - exemplar: Exemplar object to be deleted.
        returns:
        - True if the exemplar was deleted successfully, False otherwise.
        """
        if isinstance(exemplar, Exemplar):
            self._exemplar_json.remove(exemplar)
            self._save_all()
            return True
        return False
    
    def update_status(self, examplar : Exemplar) -> bool:
        """
        Updates an existing Exemplar object in the repository and saves the changes to the JSON file.
        arguments:
        - examplar: Exemplar object to be updated.
        returns:
        - True if the examplar was updated successfully, otherwise returns False.
        """
        if isinstance(examplar, Exemplar):
            self._exemplar_json[self._exemplar_json.index(examplar)] = examplar
            self._save_all()
            return True
        return False

    def check(self, attribute : str, value : object) -> bool:
        """
        Checks if a given attribute of an object is unique in the repository.
        arguments:
        - attribute: The attribute to check for uniqueness.
        - value: The value to check against the specified attribute.
        returns:
        - True if the value is unique, False if it already exists in the repository.
        """
        return any(getattr(exemplar, attribute, None) == value for exemplar in self._exemplar_json)
    
