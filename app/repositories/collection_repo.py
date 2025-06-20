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
    PATH_COLLECTION_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "collection.json"
    
    collection_json : list[Collection] = JsonStorage.load_all(PATH_COLLECTION_JSON)
    def __init__(self):
        """
        Initializes the CollectionRepo instance.
        Loads existing collections from the JSON file into the collection_json attribute.
        """
    
    def add_collection(self,name:str):
        """
        Adds a new collection with the specified name to the repository.
        The new collection is assigned a unique ID based on the current maximum ID in the repository.
        Args:
            name (str): The name of the collection to be added.
        """
        self.collection_json.append(Collection(id = None,name = name))
        JsonStorage.save_all(self.PATH_COLLECTION_JSON,self.collection_json)
        return True
    
    def get_by_name(self,name:str):
        """
        Retrieves a collection by its name from the repository.
        Args:
            name (str): The name of the collection to be retrieved.
        Returns:
            Collection: The collection object if found, None otherwise.
        """
        for collection in self.collection_json:
            if collection.name == name:
                return collection
        return None
        
    def get_by_id (self,id:int):
        """
        Retrieves a collection by its ID from the repository.
        Args:
            id (int): The ID of the collection to be retrieved.
        Returns:
            Collection: The collection object if found, None otherwise.
        """
        for collection in self.collection_json:
            if collection.id == id:
                return collection
        return None
        
    def get_all(self):
        """
        Retrieves all collections from the repository.
        Returns:
            list[Collection]: A list of all collection objects.
        """
        return self.collection_json
    
    def update_collection_by_id(self,id:int,name:str):
        """
        Updates the name of a collection by its ID.
        Args:
            id (int): The ID of the collection to be updated.
            name (str): The new name for the collection.
        Returns:
            bool: True if the collection was found and updated, False otherwise.
        """
        for collection in self.collection_json:
            if collection.id == id:
                collection.name = name
                JsonStorage.save_all(self.PATH_COLLECTION_JSON, self.collection_json)
                return True
        return False
    
    def update_collection_by_name(self,name:str,new_name:str):
        """
        Updates the name of a collection by its current name.
        Args:
            name (str): The current name of the collection to be updated.
            new_name (str): The new name for the collection.
        Returns:
            bool: True if the collection was found and updated, False otherwise.
        """
        for collection in self.collection_json:
            if collection.name == name:
                collection.name = new_name
                JsonStorage.save_all(self.PATH_COLLECTION_JSON, self.collection_json)
                return True
        return False
    
    def delete_collection(self,name:str):
        """
        Deletes a collection by its name from the repository.
        Args:
            name (str): The name of the collection to be deleted.
        Returns:
            bool: True if the collection was found and deleted, False otherwise.
        """
        for collection in self.collection_json:
            if collection.name == name:
                self.collection_json.remove(collection)
                JsonStorage.save_all(self.PATH_COLLECTION_JSON, self.collection_json)
                return True
        return False
    
    def is_unique(self, attribute : str, value : object) -> bool:
        """
        Checks if a given attribute of an object is unique in the repository.
        arguments:
        - attribute: The attribute to check for uniqueness.
        - value: The value to check against the specified attribute.
        returns:
        - True if the value is unique, False if it already exists in the repository.
        """
        return not any(getattr(collection, attribute, None) == value for collection in self.collection_json)