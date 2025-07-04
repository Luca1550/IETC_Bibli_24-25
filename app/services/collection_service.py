from repositories import CollectionRepo, BookRepo
from repositories.models import Collection

class CollectionService :
    """
    Service class for managing collections.
    This class provides methods to add, remove, and list collections.
    """
    def __init__(self):
        """
        Initializes the CollectionService with a CollectionRepo instance.
        """
        self.collection_repo = CollectionRepo()
        self.book_repo = BookRepo()
        
    def add_collection(self,name):
        """
        Adds a new collection with the given name.
        :param name: The name of the collection to add.
        :return: The newly created collection object.
        :raises Exception: If the collection name is invalid or if a collection with the same name
        """
        try:
            self._check_collection_value (name)
            if not self.collection_repo.is_unique("name",name):
                raise Exception("This collection already exists")
            return self.collection_repo.add_collection(name)
        except Exception as e:
            raise Exception(f"🛑 Error adding collection: {name} - {e}")
    
    def get_by_name(self,name):
        """
        Retrieves a collection by its name.
        :param name: The name of the collection to retrieve.
        :return: The collection object if found, None otherwise.
        """
        collection = self.collection_repo.get_by_name(name)
        if collection:
            return collection
        else : 
            return "Collection not found"
    
    def get_by_id(self,id):
        """
        Retrieves a collection by its ID.
        :param id: The ID of the collection to retrieve.
        :return: The collection object if found, None otherwise.
        """
        collection = self.collection_repo.get_by_id(id)
        if collection:
            return collection
        else : 
            return "Collection not found"
    
    def get_all(self):
        """
        Retrieves all collections.
        :return: A list of all collections.
        """
        return self.collection_repo.get_all()
    
    def update_collection_by_id(self,id:int,name:str):
        """
        Updates the name of a collection by its ID.
        :param id: The ID of the collection to update.
        :param name: The new name for the collection.
        :return: A message indicating the result of the update.
        """
        if self.collection_repo.update_collection_by_id(id,name):
            return f"Collection with ID {id} updated to {name}"
        else:
            return f"Collection with ID {id} not found"
        
    def update_collection_by_name(self,name:str,new_name:str):
        """
        Updates the name of a collection by its current name.
        :param name: The current name of the collection to update.
        :param new_name: The new name for the collection.
        :return: A message indicating the result of the update.
        """
        if self.collection_repo.update_collection_by_name(name,new_name):
            return f"Collection {name} updated to {new_name}"
        else:
            return f"Collection {name} not found"
    
    def delete_collection(self,name):
        """
        Deletes a collection by its name.
        arguments:
        - name: The name of the collection to delete.
        returns:
        - True if the deletion was successful.
        - Raises an exception if the collection is referenced elsewhere or not found.
        """
        try:
            collection = self.collection_repo.get_by_name(name)
            if isinstance(collection, Collection):
                self.delete_collection_by_id(collection.id)
        except Exception as e:
            raise Exception(f"🛑 error {e}")
        
    def delete_collection_by_id(self,id):
        """
        Deletes a collection by its ID.
        arguments:
        - id: The unique identifier of the collection.
        returns:
        - True if the deletion was successful.
        - Raises an exception if the collection is referenced elsewhere or not found.
        """
        try:
            collection = self.get_by_id(id)
            if not self.book_repo.is_unique("id_collection", collection.id):
                raise Exception("Cannot delete, already used womewhere else.")
            if self.collection_repo.delete_collection(collection.name):
                return True
            raise Exception(f"Collection ID: {id} not found")
        except Exception as e:
            raise Exception(f"🛑 error {e}")
    
    def _check_collection_value(self,name:str):
        """
        Validates the collection name.
        """
        if not name or len(name.strip())<1:
            raise Exception ("Collection cannot be empty.")
        return True