from .base import Base

class Author(Base):
    """
    Author model representing an author in the system.
    """
    def __init__(self,id:int | None,id_person:int):
        """
        Author model representing an author in the system.
        :param id: Unique identifier for the author, can be None if not yet created.
        :param id_person: Unique identifier for the person associated with the author.
        """
        super().__init__(id)
        self.id_person = id_person