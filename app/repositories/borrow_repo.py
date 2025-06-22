import pathlib
from repositories.models import Borrow
from tools import JsonStorage
class BorrowRepo:
    """""Repository for managing Borrow objects.
    This class handles the storage and retrieval of borrow records in the library system."""
    PATH_BORROW_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "borrow.json"
    borrow_json : list[Borrow] = JsonStorage.load_all(PATH_BORROW_JSON)
    
    def __init__(self):
        pass

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