from repositories.models import Person

class WorkerDTO:
    """
    Data Transfer Object for Worker.
    This class is used to transfer worker data between different layers of the application.
    """
    def __init__(self,id_worker: int, person : Person,
                ):
        """
        Initializes a WorkerDTO instance with the provided parameters.
        :param id_worker: Unique identifier for the worker.
        :param person: Person object containing personal details of the worker.
        """
        self.id_worker = id_worker
        self.person = person