import pathlib
from repositories.models import Worker
from tools import JsonStorage

class WorkerRepo:
    """
    Repository for managing Worker objects.
    arguments:
    - PATH_WORKER_JSON: Path to the JSON file where Worker data is stored.
    """
    PATH_WORKER_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "worker.json"

    _worker_json : list[Worker] = JsonStorage.load_all(PATH_WORKER_JSON)
    def __init__(self):
        """
        Initializes the WorkerRepo instance and loads all Worker data from the JSON file.
        If the JSON file does not exist, it initializes an empty list for Worker data.
        """

    def _save_all(self):
        """
        Saves all Worker data to the JSON file.
        """
        JsonStorage.save_all(self.PATH_WORKER_JSON, self._worker_json)

    def add_worker(self, worker : Worker) -> bool:
        """
        Adds a Worker object to the repository and saves it to the JSON file.
        arguments:
        - worker: Worker object to be added.
        returns:
        - True if the worker was added successfully, False otherwise.
        """
        if isinstance(worker, Worker):
            self._worker_json.append(worker)
            self._save_all()
            return True
        return False
    
    def get_by_id(self, id : int) -> Worker | bool:
        """
        Retrieves a Worker object by its ID.
        arguments:
        - id: ID of the Worker to retrieve.
        returns:
        - Returns the Worker object if found, otherwise returns False.
        """
        if id:
            return next((w for w in self._worker_json if w.id == id), None)
        return False

    def update_worker(self, worker : Worker) -> bool:
        """
        Updates an existing Worker object in the repository and saves the changes to the JSON file.
        arguments:
        - worker: Worker object to be updated.
        returns:
        - True if the worker was updated successfully, otherwise returns False.
        """
        if isinstance(worker, Worker):
            for i, w in enumerate(self._worker_json):
                if w.id == worker.id:
                    self._worker_json[i] = worker
                    self._save_all()
                    return True
        return False

    
    def delete_worker(self, worker : Worker) -> bool:
        """
        Deletes a Worker object from the repository and saves the changes to the JSON file.
        arguments:
        - worker: Worker object to be deleted.
        returns:
        - True if the worker was deleted successfully, otherwise returns False.
        """
        if isinstance(worker, Worker):
            self._worker_json = [w for w in self._worker_json if w.id != worker.id]
            self._save_all()
            return True
        return False

    def get_all_workers(self) -> list[Worker]:
        """
        Retrieves all Worker objects from the repository.
        returns:
        - A list of all Worker objects.
        """
        return self._worker_json
    
    def is_unique(self, worker: Worker) -> bool:
        """
        Checks if a Worker object is unique based on its ID.
        arguments:
        - worker: Worker object to check for uniqueness.
        returns:
        - True if the worker is unique, False otherwise.
        """
        if isinstance(worker, Worker):
            return not any(w.id == worker.id for w in self._worker_json)
        return False
