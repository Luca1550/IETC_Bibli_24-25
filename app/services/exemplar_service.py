from repositories import ExemplarRepo
from repositories.models import Exemplar
from enums import Status

class ExemplarService:
    """
    Service class for managing book exemplars.
    """

    def __init__(self):
        self._exemplar_repo : ExemplarRepo = ExemplarRepo()

    def add_exemplar(self, isbn : str, status : int, location : str):
        """
        Adds a new exemplar to the repository.
        arguments:
        - isbn: ISBN of the book.
        - status: Status of the exemplar (as an integer).
        - location: Location of the exemplar.
        returns:
        - Returns an error message if the exemplar could not be added.
        """
        try:
            self.check_exemplar_value(isbn, status, location)
            self._exemplar_repo.add_exemplar(Exemplar(
                id=None,
                isbn=isbn,
                status=Status(status),
                location=location
            ))
        except Exception as e:
            raise Exception(f"error : {e}")
        
    def check_exemplar_value(self, isbn : str, status : int, location : str):
        """
        Checks if the values provided for adding an exemplar are valid.
        arguments:
        - isbn: ISBN of the book.
        - status: Status of the exemplar (as an integer).
        - location: Location of the exemplar.
        raises:
        - Exception if any of the values are invalid.
        """
        if not isbn:
            raise Exception(f"Isbn cannot be empty.")
        if status not in [s.value for s in Status]:
            raise Exception(f"Invalid status")
        if not location:
            raise Exception(f"Location cannot be empty.")
    
    def get_by_id(self, id:int):
        """
        Retrieves an exemplar by its ID.
        """
        exemplar = self._exemplar_repo.get_by_id(id)
        if isinstance(exemplar, Exemplar):
            return exemplar
        raise Exception("Not found")
