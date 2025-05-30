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
    
    def get_by_id(self, id: int) -> Worker | str:
        """ 
        Retrieves a Worker by their ID.
        arguments:
        - id: ID of the Worker to retrieve.
        returns:
        - Returns the Worker object if found, otherwise returns an error message.
        """
        worker = self._worker_repo.get_by_id(id)
        if worker:
            return worker
        return "Worker not found."
    
    def get_worker_authorization(self, id: int) -> bool:
        """
        Retrieves the authorization status of a Worker by their ID.
        arguments:
        - id: ID of the Worker to check.
        returns:
        - True if the Worker has authorization, False otherwise.
        """
        return self._worker_repo.get_authorization(id)


