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
            self.collection_repo.add_theme(name)
        except:
            print(f"Error adding collection: {name}")
            return f"Error adding collection: {name}"