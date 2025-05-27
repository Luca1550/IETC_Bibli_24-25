from repositories.models import Collection
from tools import JsonStorage
import pathlib

class CollectionRepo:
    """
    Repository for managing collections.
    Provides methods to load, add, and save collections.
    Attributes:
        PATH_COLLECTIOB_JSON (pathlib.Path): Path to the JSON file storing collections.
    """
    PATH_COLLECTIOB_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "collection.json"
    
    def __init__(self):
        """
        Initializes the CollectionRepo instance.
        Loads existing collections from the JSON file into the collection_json attribute.
        """
        self.collection_json : list[Collection] = JsonStorage.load_all(self.PATH_COLLECTIOB_JSON)
    
    def add_theme(self,name:str):
        """
        Adds a new collection with the specified name to the repository.
        The new collection is assigned a unique ID based on the current maximum ID in the repository.
        Args:
            name (str): The name of the collection to be added.
        """
        self.collection_json.append(Collection(id = None,name = name))
        JsonStorage.save_all(self.PATH_COLLECTIOB_JSON,self.collection_json)