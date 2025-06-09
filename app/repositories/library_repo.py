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
    
    def update_library(self,library: Library):  
        """
        Updates an existing library in the repository.
        Args:
            library (Library): The Library object containing the updated values.
        Returns:
            bool: True if the library was updated successfully, False otherwise.
        """
        for i, lib in enumerate(self.library_json):
            if isinstance(lib, dict):
                    if lib.get('id') == library.id:
                        self.library_json[i] = library.__dict__  
                        self._save_all()
                        return True
        return False