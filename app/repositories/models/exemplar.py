from .base import Base
from enums import Status

class Exemplar(Base):
    def __init__(self, id : int, isbn : str, status : Status, location : str):
        super().__init__(id)
        self.isbn = isbn
        self.status = status
        self.location = location 