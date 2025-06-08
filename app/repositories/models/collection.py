from .base import Base

class Collection(Base):
    """
    Represents a collection with a unique ID and a name.
    inherits from Base to ensure each collection has a unique identifier.
    """
    def __init__(self,id:int | None,name : str):
        """
        Initializes a new Collection instance with a unique ID and a name.
        If an ID is provided, it will be used; otherwise, a new unique ID is generated.
        Args:
            id (int | None): Unique identifier for the collection. If None, a new ID is generated.
            name (str): Name of the collection.
        """
        super().__init__(id)
        self.name = name

    def __eq__(self, other):
        """
        Compares two Collection objects for equality based on their ID.
        arguments:
            other (Collection): The other Collection object to compare with.
        """
        if isinstance(other, Collection):
            return self.id == other.id

    def __hash__(self):
        """
        Returns a hash value for the Collection object based on its ID.
        """
        return hash(self.id)