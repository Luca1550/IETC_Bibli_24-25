from repositories.models import Base

class Worker(Base):
    def __init__(self, id: int | None, id_person: int , authorization : bool):
        """
        Worker model representing a worker in the system.
        :param id: Unique identifier for the worker, can be None if not yet created.
        :param id_person: Unique identifier for the associated person.
        """
        super().__init__(id)
        self.id_person = id_person
        self.authorization = authorization