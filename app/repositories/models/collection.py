from .base import Base

class Collection(Base):
    """
    Represents a collection with a unique ID and a name.
    inherits from Base to ensure each collection has a unique identifier.
    Attributes:
        id (int | None): Unique identifier for the collection.
        name (str): Name of the collection.
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