from repositories import CollectionRepo

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
        
    def add_collection(self,name):
        """
        Adds a new collection with the given name.
        :param name: The name of the collection to add.
        :return: None
        """
        try:
            self.collection_repo.add_collection(name)
        except:
            return f"Error adding collection: {name}"
    
    def get_by_collection(self,name):
        """
        Retrieves a collection by its name.
        :param name: The name of the collection to retrieve.
        :return: The collection object if found, None otherwise.
        """
        collection = self.collection_repo.get_by_collection(name)
        if collection:
            return f"Collection : {collection.name}"
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
            return f"Collection : {collection.name}"
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
        Deletes a collection with the given name.
        :param name: The name of the collection to delete.
        :return: A message indicating the result of the deletion.
        """
        if self.collection_repo.delete_collection(name):
            return f"Collection : {name} deleted"
        else:
            return f"Collection : {name} not found"