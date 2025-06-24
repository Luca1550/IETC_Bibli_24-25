from .base import Base
from enums import Status

class Exemplar(Base):
    """
    Represents a book in the library system.
    Each exemplar has a unique ID, an ISBN, a status indicating its availability,
    and a location within the library.
    """
    def __init__(self, id : int, isbn : str, status : Status, location : str):
        super().__init__(id)
        self.isbn = isbn
        self.status = status
        self.location = location 