from .base import Base

class Author(Base):
    
    def __init__(self,id:int | None,id_person:int):
        super().__init__(id)
        self.id_person = id_person