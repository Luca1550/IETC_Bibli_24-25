import re
from repositories.models import Worker
from repositories import WorkerRepo

class WorkerService:
    """
    Service for managing Worker objects.
    """
    def __init__(self):
        """
        Initializes the WorkerService instance with a WorkerRepo instance.
        """
        self._worker_repo: WorkerRepo = WorkerRepo()

    def add_worker(self, id_person: int, authorization: bool) -> Worker | str:
        """
        Adds a new Worker to the repository.
        arguments:
        - id_person: ID of the person associated with the worker.
        - authorization: Boolean indicating if the worker has authorization.
        returns:
        - Returns the newly created Worker object if successful, otherwise returns an error message.
        """
        new_worker = Worker(id=None, id_person=id_person, authorization=authorization)
        if self._worker_repo.is_unique_worker(new_worker):
            self._worker_repo.add_worker(new_worker)
            return new_worker
        return "Worker already exists."