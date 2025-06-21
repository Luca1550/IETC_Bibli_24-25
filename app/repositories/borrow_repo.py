import pathlib
from repositories.models import Borrow
from tools import JsonStorage
from datetime import datetime,date
from enums import Paiement_type
class BorrowRepo:
    """""Repository for managing Borrow objects.
    This class handles the storage and retrieval of borrow records in the library system."""
    PATH_BORROW_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "borrow.json"
    borrow_json : list[Borrow] = JsonStorage.load_all(PATH_BORROW_JSON)
    
    def __init__(self):
        """Initializes the BorrowRepository instance and loads all borrow data from the JSON file.
        If the JSON file does not exist, it initializes an empty list for borrow data."""
        self.borrow_json : list[Borrow] = JsonStorage.load_all(self.PATH_BORROW_JSON)
        if self.borrow_json is None:
            self.borrow_json = []

    def add_borrow(self, borrow: Borrow):
        """Adds a Borrow object to the repository and saves it to the JSON file.
        arguments: 
        - borrow: Borrow object to be added.
        returns:
        - True if the borrow was added successfully, False otherwise."""
        if borrow:
            self.borrow_json.append(borrow)
            self._save_all()
            return True
        return False 

    def get_borrows(self):
        """Retrieves all Borrow objects from the repository.
        returns:
        - A list of Borrow objects."""
        return self.borrow_json
    def get_by_id(self,id):
        for borrow in self.borrow_json:
            if borrow.id == id:
                return borrow
        return None

    def update_borrow(self, borrow: Borrow):
        """Updates an existing Borrow object in the repository and saves the changes to the JSON file.
        arguments:
        - borrow: Borrow object to be updated.
        returns:
        - True if the borrow was updated successfully, otherwise returns False."""
        if isinstance(borrow, Borrow):
            self.borrow_json[self.borrow_json.index(borrow)] = borrow
            self._save_all()
            return True
        return False

    def delete_borrow(self, borrow: Borrow):
        """Deletes a Borrow object from the repository and saves the changes to the JSON file.
        arguments:
        - borrow: Borrow object to be deleted.
        returns:
        - True if the borrow was deleted successfully, otherwise returns False."""
        if isinstance (borrow, Borrow):
            self.borrow_json.remove(borrow)
            self._save_all()
            return True
        return False
    
    # def check_limit_borrow(self,limit_borrow:int,id_member:int):
    #     """Checks if the number of borrows is below the specified limit.
    #     arguments:
    #     - limit_borrow: The maximum number of borrows allowed.
    #     returns:
    #     - True if the number of borrows is below the limit, False otherwise."""
    #     if id_member:
    #         #chek ddans le json de borrow si nb de fois qu'il y a le meme id_member dedans est < limit_borrow
    #         for bor in self._borrow_member_json:
    #             if bor.member
    #     return False
    #     return len(self.borrow_json) < limit_borrow
    def calculate_fine(self, return_date:date, borrow_date:date,fine_per_day:int):
        """Calculates the fine for overdue borrows.
        arguments:
        - return_date: The date the item was returned.
        - borrow_date: The date the item was borrowed.
        - fine_per_day: The fine amount per day of delay.
        returns:
        - The total fine amount if the item is overdue, otherwise returns 0."""
        if return_date and borrow_date:
            days_overdue = (return_date - borrow_date).days
            if days_overdue > 0:
                fine =days_overdue * fine_per_day
                return fine
    
    def _save_all(self):
        """Saves all borrow data to the JSON file.
        This method is called after adding, updating, or deleting a borrow record to ensure that the changes are persisted."""

        JsonStorage.save_all(self.PATH_BORROW_JSON, self.borrow_json)  
    
    def is_unique(self,attribute:str,value:object):
        """Checks if a given attribute of a Borrow object is unique in the repository.
        arguments:
        - attribute: The attribute to check for uniqueness (e.g., 'id_exemplar', 'borrow_date').
        - value: The value to check against the specified attribute.
        returns:
        - True if the value is unique, False otherwise.
        """ 
        #merci luca pour celle la 
        return not any (getattr(id,attribute,None)== value for id in self.borrow_json)