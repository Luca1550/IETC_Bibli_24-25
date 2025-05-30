import pathlib
from repositories.models import Person
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

    def add_person(self, person : Person) -> bool:
        """
        Adds a Person object to the repository and saves it to the JSON file.
        arguments:
        - person: Person object to be added.
        returns:
        - True if the person was added successfully, False otherwise.
        """
        if isinstance(person, Person):
            self._person_json.append(person)
            self._save_all()
            return True
        return False
    
    def get_by_id(self, id : int) -> Person | bool:
        """
        Retrieves a Person object by its ID.
        arguments:
        - id: ID of the Person to retrieve.
        returns:
        - Returns the Person object if found, otherwise returns False.
        """
        if id:
            return next((p for p in self._person_json if p.id == id), None)
        return False
    
    def update_person(self, person : Person) -> bool:
        """
        Updates an existing Person object in the repository and saves the changes to the JSON file.
        arguments:
        - person: Person object to be updated.
        returns:
        - True if the person was updated successfully, otherwise returns False.
        """
        if isinstance(person, Person):
            self._person_json[self._person_json.index(person)] = person
            self._save_all()
            return True
        return False

    def delete_person(self, person : Person) -> bool:
        """
        Deletes a Person object from the repository and saves the changes to the JSON file.
        arguments:
        - person: Person object to be deleted.
        returns:
        - True if the person was deleted successfully, False otherwise.
        """
        if isinstance(person, Person):
            self._person_json.remove(person)
            self._save_all()
            return True
        return False
    
    def is_unique(self, attribute : str, value : object) -> bool:
        """
        Checks if a given attribute of a Person object is unique in the repository.
        arguments:
        - attribute: The attribute to check for uniqueness (e.g., 'national_number', 'email').
        - value: The value to check against the specified attribute.
        returns:
        - True if the value is unique, False if it already exists in the repository.
        """
        return not any(getattr(person, attribute, None) == value for person in self._person_json)
