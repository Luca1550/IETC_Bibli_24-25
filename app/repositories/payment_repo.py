import pathlib
from repositories.models import Payment
from tools import JsonStorage

class PaymentRepo:
    """Repository for managing payment objects, providing methods to add, update, delete, and retrieve payment data.
    This class handles the storage and retrieval of payment records in the library system."""
    PATH_PAYMENT_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "payment.json"

    _payment_json : list[Payment] = JsonStorage.load_all(PATH_PAYMENT_JSON)
    def __init__(self):
        """Initializes the PaymentRepo instance and loads all payment data from the JSON file."""

    def _save_all(self):
        """Saves all payment data to the JSON file.
        This method is called after any modification to the payment data to ensure that changes are persisted."""
        JsonStorage.save_all(self.PATH_PAYMENT_JSON, self._payment_json)

    def add_payment(self, payment : Payment) :
        """Adds a payment object to the repository and saves it to the JSON file.
        arguments:
        - payment: payment object to be added."""
        if isinstance(payment, Payment):
            self._payment_json.append(payment)
            self._save_all()
            return True
        return False
    
    def get_by_id(self, id : int):
        """
        Retrieves a payment object by its ID.
        arguments:
        - id: ID of the payment to retrieve.
        returns:
        - Returns the payment object if found, otherwise returns False.
        """
        if id:
            return next((p for p in self._payment_json if p.id == id), None)
        return False
    
    def get_payment_parameters(self):
        """ Retrieves all payment objects from the repository.
        returns: A list of all payment objects.
        """
        return self._payment_json

    def update_payment(self, payment : Payment) -> bool:
        """
        Updates an existing payment object in the repository and saves the changes to the JSON file.
        arguments:
        - payment: payment object to be updated.
        returns:
        - True if the payment was updated successfully, otherwise returns False.
        """
        if isinstance(payment, Payment):
            self._payment_json[self._payment_json.index(payment)] = payment
            self._save_all()
            return True
        return False

    def delete_payment(self, payment : Payment) -> bool:
        """
        Deletes a payment object from the repository and saves the changes to the JSON file.
        arguments:
        - payment: payment object to be deleted.
        """
        if isinstance(payment, Payment):
            self._payment_json.remove(payment)
            self._save_all()
            return True
        return False
    