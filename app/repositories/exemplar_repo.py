from .models import Exemplar
from tools import JsonStorage
import pathlib

class ExemplarRepo():
    """
    Repository class for managing book exemplars.
    """
    PATH_EXEMPLAR_JSON = pathlib.Path(__file__).parent.parent.parent / "database" / "exemplar.json"

    def __init__(self):
        """
        Initializes the ExemplarRepo and loads all exemplars from the JSON file.
        """
        self._exemplar_json : list[Exemplar] = JsonStorage.load_all(self.PATH_EXEMPLAR_JSON)
    
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