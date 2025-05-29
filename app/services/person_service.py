import re
from repositories.models import Person
from repositories import PersonRepo

class PersonService:
    """
    Service for managing Person objects.
    """
    def __init__(self):
        """
        Initializes the PersonService instance with a PersonRepo instance.
        """
        self._person_repo : PersonRepo = PersonRepo()
    
    def add_person(self, first_name : str, last_name : str, national_number: str, email : str, street : str, cp : str, city : str) -> Person | str:
        """
        Adds a new person to the repository.
        arguments:
        - first_name: First name of the person.
        - last_name: Last name of the person.
        - national_number: National number (NISS) of the person.
        - email: Email address of the person.
        - street: Street address of the person.
        - cp: Postal code of the person's address.
        - city: City of the person's address.
        returns:
        - Returns an error message if there was an issue adding the person.
        """
        try:
            if not len(national_number) == 11 or not national_number.isnumeric():
                raise Exception("Invalid national number: it must be exactly 11 characters long and numeric value.")
            if self._person_repo.person_niss_exist(national_number):
                raise Exception("Person already exists: The provided national number is already registered.")
            if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                raise Exception("Invalid email format: Please enter a valid email address.")
            if not cp.isnumeric() or not len(cp) >= 4:
                raise Exception("Invalid postal code format: It must be a numeric value with at least 4 digits.")
            new_person = Person(
                    id=None,
                    first_name=first_name,
                    last_name=last_name,
                    national_number=national_number,
                    email=email,
                    street=street,
                    cp=cp,
                    city=city
                )
            if self._person_repo.add_person(new_person):
                return new_person
        except Exception as e:
            return f"🛑 Error [{e}]"
        
    def get_by_id(self, id : int):
        """
        Retrieves a person by their ID.
        arguments:
        - id: ID of the person to retrieve.
        returns:
        - Returns the Person object if found, otherwise raises an exception.
        """
        try:
            get_person = self._person_repo.get_by_id(id)
            if get_person:
                return get_person
            else:
                raise Exception(f"Person with the given ID : {id} was not found.")
        except Exception as e:
            return f"🛑 Error [{e}]"