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

    def delete_worker(self, id: int) -> bool:
        """
        Deletes a worker by their ID.
        arguments:
        - id: ID of the worker to delete.
        returns:
        - True if the worker was deleted successfully, False otherwise.
        """
        try:
            worker = self._worker_repo.get_by_id(id)
            if worker:
                self._worker_repo.delete_worker(worker)
                return True
            else:
                raise Exception(f"Worker with the given ID : {id} was not found.")
        except Exception as e:
            print(f"🛑 Error [{e}]")
            return False