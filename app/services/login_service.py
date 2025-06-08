import re
from repositories.models import Login
from repositories import LoginRepo

class LoginService:
    """
    Service for managing Login objects.
    """
    def __init__(self, login_repo: LoginRepo):
        """
        Initializes the LoginService instance with a LoginRepo.
        arguments:
        - login_repo: LoginRepo instance for managing login data.
        """
        self._login_repo = login_repo

    def create_login(self, worker_id: int, username: str, password: str) -> Login | None:
        """
        Creates a new Login object and adds it to the repository.
        arguments:
        - worker_id: ID of the associated worker.
        - username: Username for the login.
        - password: Password for the login.
        returns:
        - The created Login object if successful, otherwise returns None.
        """
        login = Login(None, worker_id, username, password)
        if self._login_repo.add_login(login):
            return login
        return None

    def delete_login(self, login: Login) -> bool:
        """
        Deletes a Login object from the repository.
        arguments:
        - login: Login object to be deleted.
        returns:
        - True if the login was deleted successfully, otherwise returns False.
        """
        return self._login_repo.delete_login(login)

    def update_login(self, login: Login) -> bool:
        """
        Updates an existing Login object in the repository.
        arguments:
        - login: Login object to be updated.
        returns:
        - True if the login was updated successfully, otherwise returns False.
        """
        return self._login_repo.update_login(login)

    def get_login_by_worker_id(self, worker_id: int) -> Login | None:
        """
        Retrieves a Login object by the associated worker ID.
        arguments:
        - worker_id: ID of the worker whose login is to be retrieved.
        returns:
        - The Login object if found, otherwise returns None.
        """
        return self._login_repo.get_by_worker_id(worker_id)

    def get_login_by_id(self, id: int) -> Login | None:
        """
        Retrieves a Login object by its ID.
        arguments:
        - id: ID of the login to be retrieved.
        returns:
        - The Login object if found, otherwise returns None.
        """
        return self._login_repo.get_by_id(id)
