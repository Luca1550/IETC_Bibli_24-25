import re
from repositories.models import Worker
from repositories.models import Person
from repositories import WorkerRepo
from repositories import PersonRepo

class WorkerService:
    """
    Service for managing Worker objects.
    """
    def __init__(self):
        """
        Initializes the WorkerService instance with a WorkerRepo instance.
        """
        self._worker_repo: WorkerRepo = WorkerRepo()

    def add_worker(self, person:Person) -> Worker | str:
        """
        Adds a new worker to the repository.
        arguments:
        - person: Person object containing worker details.
        returns:
        - Returns a Worker object if added successfully, otherwise returns an error message.
        """
        try:
            if isinstance(person, Person):
                new_worker = Worker(
                    id=None,
                    first_name=person.first_name,
                    last_name=person.last_name,
                    national_number=person.national_number,
                    email=person.email,
                    street=person.street,
                    cp=person.cp,
                    city=person.city
                )
                if self._worker_repo.add_worker(new_worker):
                    return new_worker
            else:
                raise TypeError("Provided person is not a valid Person object.")
        except Exception as e:
            return f"🛑 Error [{e}]"

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
    
    def get_by_id(self, id: int) -> Worker | str:
        """
        Retrieves a worker by their ID.
        arguments:
        - id: ID of the worker to retrieve.
        returns:
        - Returns the Worker object if found, otherwise returns an error message.
        """
        try:
            worker = self._worker_repo.get_by_id(id)
            if worker:
                return worker
            else:
                raise Exception(f"Worker with the given ID : {id} was not found.")
        except Exception as e:
            return f"🛑 Error [{e}]"

