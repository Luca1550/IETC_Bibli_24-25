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
    
    def add_person(self, first_name : str, last_name : str | None, national_number: str | None, email : str | None, street : str | None, cp : str | None, city : str | None) -> Person | Exception:
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
            if self._check_person_value(national_number, email, cp):
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
            raise Exception(f"🛑 Error {e}")
        
    def get_by_id(self, id : int) -> Person | str:
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
            raise Exception(f"🛑 Error {e}")
        
    def update_person(self, id : int, first_name : str, last_name : str | None, national_number: str | None, email : str | None, street : str | None, cp : str | None, city : str | None) -> bool | str:
        try:
            person = self.get_by_id(id)
            if not isinstance(person, Person):
                raise Exception(person)
            if self._check_person_value((national_number if national_number != person.national_number else None), email, cp):
                person.first_name = first_name or person.first_name
                person.last_name = (last_name or person.last_name) if last_name is not None else None
                person.national_number = (national_number or person.national_number) if national_number is not None else None
                person.email = (email or person.email) if email is not None else None
                person.street = (street or person.street) if street is not None else None
                person.cp = (cp or person.cp) if cp is not None else None
                person.city = (city or person.city) if city is not None else None
                if self._person_repo.update_person(person):
                    return True
        except Exception as e:
            raise Exception(f"🛑 Error {e}")
        
    def delete_person(self, id : int) -> bool | str:
        """
        Deletes a person by their ID.
        arguments:
        - id: ID of the person to delete.
        returns:
        - True if the person was deleted successfully, False otherwise.
        """
        try:
            person = self.get_by_id(id)
            if isinstance(person, Person):
                return self._person_repo.delete_person(person)
            raise Exception(person)
        except Exception as e:
            raise Exception(f"🛑 Error {e}")
        
    def _check_person_value(self, national_number: str | None, email: str | None, cp: str | None) -> Exception | bool:
        if national_number:
            if len(national_number) != 11 or not national_number.isnumeric():
                raise Exception("Invalid national number: it must be exactly 11 characters long and numeric value.")
            if not self._person_repo.is_unique("national_number", national_number):
                raise Exception("Person already exists: The provided national number is already registered.")
        if email:
            if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                raise Exception("Invalid email format: Please enter a valid email address.")
        if cp:
            if not cp.isnumeric()  or not (4 <= len(cp) <= 5):
                raise Exception("Invalid postal code format: It must be a numeric value with at least 4 digits.")
        return True
