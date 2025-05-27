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
    
    def add_person(self, first_name : str, last_name : str, national_number: str, email : str, street : str, cp : str, city : str):
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
        """
        try:
            if not len(national_number) == 11:
                raise Exception("Invalid national number: it must be exactly 11 characters long.")
            if self._person_repo.person_niss_exist(national_number):
                raise Exception("Person already exists: The provided national number is already registered.")
            if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                raise Exception("Invalid email format: Please enter a valid email address.")
            if self._person_repo.add_person(
                Person(
                    id=None,
                    first_name=first_name,
                    last_name=last_name,
                    national_number=national_number,
                    email=email,
                    street=street,
                    cp=cp,
                    city=city
                )):
                return print(f"Person {first_name} {last_name} added successfully. ✅")
        except Exception as e:
            return print(f"🛑 Error : {e}")