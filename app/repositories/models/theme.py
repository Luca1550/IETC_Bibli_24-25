from .base import Base

class Theme(Base):
    """
    Represents a theme with a unique ID and a name.
    Inherits from Base to ensure each theme has a unique identifier.
    """
    def __init__(self,id:int | None,name : str):
        """
        Initializes a new Theme instance with a unique ID and a name.
        If an ID is provided, it will be used; otherwise, a new unique ID is generated.
        Args:
            id (int | None): Unique identifier for the theme. If None, a new ID is generated.
            name (str): Name of the theme.
        """
        super().__init__(id)
        self.name = name

    def __eq__(self, other):
        """
        Compares two Theme objects for equality based on their ID.
        arguments:
            other (Theme): The other Theme object to compare with.
        """
        if isinstance(other, Theme):
            return self.id == other.id

    def __hash__(self):
        """
        Returns a hash value for the Theme object based on its ID.
        """
        return hash(self.id)