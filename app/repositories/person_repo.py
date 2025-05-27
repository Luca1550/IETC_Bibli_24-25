import pathlib
from models import Person
from tools import JsonStorage

class PersonRepo:
    """
    Repository for managing Person objects.
    arguments:
    - PATH_PERSON_JSON: Path to the JSON file where Person data is stored.
    """
    PATH_PERSON_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "person.json"

    def __init__(self):
        """
        Initializes the PersonRepo instance and loads all Person data from the JSON file.
        If the JSON file does not exist, it initializes an empty list for Person data.
        """
        self._person_json : list[Person] = JsonStorage.load_all(self.PATH_PERSON_JSON)

    def _save_all(self):
        """
        Saves all Person data to the JSON file.
        """
        JsonStorage.save_all(self.PATH_PERSON_JSON, self._person_json)

    def add_person(self, person : Person):
        """
        Adds a Person object to the repository and saves it to the JSON file.
        arguments:
        - person: Person object to be added.
        returns:
        - True if the person was added successfully, False otherwise.
        """
        if person:
            self._person_json.append(person)
            self._save_all()
            return True
        return False
