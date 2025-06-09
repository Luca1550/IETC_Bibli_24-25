from .base import Base

class Editor(Base):
    """
    Represents a editor with a unique ID and a name.
    inherits from Base to ensure each editor has a unique identifier.
    """
    def __init__(self,id:int | None,name : str):
        """
        Initializes a new editor instance with a unique ID and a name.
        If an ID is provided, it will be used; otherwise, a new unique ID is generated.
        Args:
            id (int | None): Unique identifier for the editor. If None, a new ID is generated.
            name (str): Name of the editor.
        """
        super().__init__(id)
        self.name = name

    def __eq__(self, other):
        """
        Compares two Editor objects for equality based on their ID.
        arguments:
            other (Editor): The other Editor object to compare with.
        """
        if isinstance(other, Editor):
            return self.id == other.id

    def __hash__(self):
        """
        Returns a hash value for the Editor object based on its ID.
        """
        return hash(self.id)