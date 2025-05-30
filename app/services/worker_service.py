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

    def update_worker(self, worker: Worker) -> bool:
        """
        Updates an existing worker in the repository.
        arguments:
        - worker: Worker object to be updated.
        returns:
        - True if the worker was updated successfully, otherwise returns False.
        """
        if isinstance(worker, Worker):
            return self._worker_repo.update_worker(worker)
        return False
        
