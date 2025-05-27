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
            print(f"Error adding collection: {name}")
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
            return "Collection non trouvé"
    
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
            return "Collection non trouvé"
    
    def get_all(self):
        """
        Retrieves all collections.
        :return: A list of all collections.
        """
        return self.collection_repo.get_all()