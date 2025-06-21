import pathlib
from repositories.models import Login
from tools import JsonStorage

class LoginRepo:
    """
    Repository for managing Login objects.
    arguments:
    - PATH_LOGIN_JSON: Path to the JSON file where Login data is stored.
    """
    PATH_LOGIN_JSON = pathlib.Path(__file__).parent.parent.parent / "database" / "login.json"

    _login_json: list[Login] = JsonStorage.load_all(PATH_LOGIN_JSON)
    def __init__(self):
        """
        Initializes the LoginRepo instance and loads all Login data from the JSON file.
        If the JSON file does not exist, it initializes an empty list for Login data.
        """

    def _save_all(self):
        """
        Saves all Login data to the JSON file.
        """
        JsonStorage.save_all(self.PATH_LOGIN_JSON, self._login_json)

    def add_login(self, login: Login) -> bool:
        """
        Adds a Login object to the repository and saves it to the JSON file.
        arguments:
        - login: Login object to be added.
        returns:
        - True if the login was added successfully, False otherwise.
        """
        if isinstance(login, Login):
            self._login_json.append(login)
            self._save_all()
            return True
        return False
    
    def delete_login(self, login: Login) -> bool:
        """
        Deletes a Login object from the repository and saves the changes to the JSON file.
        arguments:
        - login: Login object to be deleted.
        returns:
        - True if the login was deleted successfully, otherwise returns False.
        """
        if isinstance(login, Login):
            self._login_json.remove(login)
            self._save_all()
            return True
        return False
    
    def update_login(self, login: Login) -> bool:
        """
        Updates an existing Login object in the repository and saves the changes to the JSON file.
        arguments:
        - login: Login object to be updated.
        returns:
        - True if the login was updated successfully, otherwise returns False.
        """
        if isinstance(login, Login):
            for i, existing_login in enumerate(self._login_json):
                if existing_login.id == login.id:
                    self._login_json[i] = login
                    self._save_all()
                    return True
        return False
    
    def get_by_worker_id(self, id: int) -> Login | None:
        """
        Retrieves a Login object by the associated worker ID.
        arguments:
        - id: ID of the worker whose login is to be retrieved.
        returns:
        - The Login object if found, otherwise returns None.
        """
        for login in self._login_json:
            if login.worker_id == id:
                return login
        return None

    def get_by_id(self, id: int) -> Login | None:
        """
        Retrieves a Login object by its ID.
        arguments:
        - id: ID of the login to be retrieved.
        returns:
        - The Login object if found, otherwise returns None.
        """
        for login in self._login_json:
            if login.id == id:
                return login
        return None