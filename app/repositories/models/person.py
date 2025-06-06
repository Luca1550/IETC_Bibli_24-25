from repositories.models import Base

class Person(Base):
    """
    Represents a person with personal details such as name, contact information, and address.
    """
    def __init__(self, id : int | None, first_name : str, last_name : str, national_number : str, email : str, street : str, cp : str, city : str):
        """
        Initializes a new Person instance with the provided attributes.
        Args:
            id (int | None): Unique identifier for the person. If None, a new ID is generated.
            first_name (str): First name of the person.
            last_name (str): Last name of the person.
            national_number (str): National identification number.
            email (str): Email address of the person.
            street (str): Street address of the person.
            cp (str): Postal code of the person's address.
            city (str): City of the person's address.
        """
        super().__init__(id)
        self.first_name = first_name
        self.last_name = last_name
        self.national_number = national_number
        self.email = email
        self.street = street
        self.cp = cp
        self.city = city