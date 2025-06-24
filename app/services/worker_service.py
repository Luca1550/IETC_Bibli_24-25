from services.models import WorkerDTO
from repositories.models import Worker,Person
from repositories import WorkerRepo, PersonRepo
from services import PersonService


class WorkerService:
    """
    Service for managing Worker objects.
    """
    def __init__(self):
        """
        Initializes the WorkerService instance with a WorkerRepo instance.
        """
        self._worker_repo: WorkerRepo = WorkerRepo()
        self._person_repo: PersonRepo = PersonRepo()
        self._person_service = PersonService()

    def add_worker(self, id : int, first_name : str, last_name : str, national_number: str, email : str, street : str, cp : str, city : str) -> WorkerDTO | str:
        """
        Adds a new worker to the repository.
        arguments:
        - person: Person object containing worker details.
        returns:
        - Returns a Worker object if added successfully, otherwise returns an error message.
        """
        try:
            person = self._person_service.add_person(
                first_name,
                last_name,
                national_number,
                email,
                street,
                cp,
                city
            )
            if isinstance(person, Person):
                worker = Worker(
                    id=None,  # ID will be assigned by the repository
                    id_person=person.id,
                )
                self._worker_repo.add_worker(worker)
                return WorkerDTO(id_worker=worker.id, person=person)
            else:
                raise Exception("Failed to add person.")
        except Exception as e:
            raise(f"🛑 Error [{e}]")
            raise Exception(str(e))

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
                self._person_service.delete_person(worker.id_person)
                return True
            else:
                raise Exception(f"Worker with the given ID : {id} was not found.")
        except Exception as e:
            raise(f"🛑 Error [{e}]")
            return False

    def update_worker(self, id : int, first_name : str, last_name : str, national_number: str, email : str, street : str, cp : str, city : str) -> bool | str:
        """
        Updates an existing worker in the repository.
        arguments:
        - worker: Worker object to be updated.
        returns:
        - True if the worker was updated successfully, otherwise returns False.
        """
    
        if self._person_service.update_person(
            id,
            first_name,
            last_name,
            national_number,
            email,
            street,
            cp,
            city
        ): 
            return True
        raise Exception("Worker not found or update failed.")
    
    def get_worker_by_id(self, id: int) -> WorkerDTO | str:
        """
        Retrieves a worker by their ID.
        arguments:
        - id: ID of the worker to retrieve.
        returns:
        - Returns a WorkerDTO object if found, otherwise raises an exception.
        """
        try:
            worker = self._worker_repo.get_by_id(id)
            if worker:
                person = self._person_repo.get_by_id(worker.id_person)
                if person:
                    return WorkerDTO(
                        id_worker=worker.id,
                        person=person
                    )
                else:
                    raise Exception(f"Person associated with worker ID {id} not found.")
            else:
                raise Exception(f"Worker with the given ID : {id} was not found.")
        except Exception as e:
            raise(f"🛑 Error [{e}]")
            raise Exception(f"🛑 Error [{e}]")
        
    def get_all_workers(self) -> list[WorkerDTO]:
        """
        Retrieves all workers from the repository.
        returns:
        - Returns a list of WorkerDTO objects representing all workers.
        """
        try:
            workers = self._worker_repo.get_all_workers()
            worker_dtos = []
            for worker in workers:
                person = self._person_repo.get_by_id(worker.id_person)
                if person:
                    worker_dtos.append(WorkerDTO(
                        id_worker=worker.id,
                        person=person
                    ))
            return worker_dtos
        except Exception as e:
            raise(f"🛑 Error [{e}]")
            raise Exception(f"🛑 Error [{e}]")

