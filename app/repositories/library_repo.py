import pathlib
from repositories.models import Library
from tools import JsonStorage

class LibraryRepo:
    """
    Repository for managing libraries.
    Provides methods to load, add, and save libraries.
    """

    PATH_LIBRARY_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "library.json"

    def __init__(self):
        """
        Initializes the Libraryrepo instance.
        Loads existing libraries from the JSON file into the library_json attribute.
        """
        self.library_json : list[Library] = JsonStorage.load_all(self.PATH_LIBRARY_JSON)
        
    def _save_all(self):
        """
        Saves all libraries to the JSON file.
        This method is called after any modification to the library data.
        """
        JsonStorage.save_all(self.PATH_LIBRARY_JSON, self.library_json)

    def get_library_parameters(self):
        """
        Retrieves the parameters of the library.
        Returns:
            list[Library]: A list of library objects.
        """
        
        return self.library_json
    
    def add_library(self, library: Library):
        """
        Adds a new library to the repository.
        Args:
            library (Library): The Library object to be added.
        """
        if library:
            self.library_json.append(library)
            self._save_all()
            return True
        return False
    
    def update_library(self, id:int,name:str,fine_per_day:float,subscribe_amout:float,limit_borrow:int,borrow_price_with_sub:float,borrow_price_without_sub:float,borrow_delay:int,url_logo:str): 
        """
        Updates an existing library in the repository.
        Args:
            id (int): The ID of the library to update.
            name (str): The new name of the library.
            fine_per_day (float): The new fine per day for overdue items.
            subscribe_amout (float): The new subscription amount for the library.
            limit_borrow (int): The new maximum number of items that can be borrowed at once.
            borrow_price_with_sub (float): The new borrowing price for subscribers.
            borrow_price_without_sub (float): The new borrowing price for non-subscribers.
            borrow_delay (int): The new allowed borrowing delay in days.
            url_logo (str): The new URL to the library's logo image.

        """
        for library in self.library_json:
            if library.id == id:
                library.name = name
                library.fine_per_day = fine_per_day
                library.subscribe_amout = subscribe_amout
                library.limit_borrow = limit_borrow
                library.borrow_price_with_sub = borrow_price_with_sub
                library.borrow_price_without_sub = borrow_price_without_sub
                library.borrow_delay = borrow_delay
                library.url_logo = url_logo
                self._save_all()  
                return True
        return False