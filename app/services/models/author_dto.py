from repositories.models import  Person

class AuthorDTO:
    """
    Data Transfer Object for Author.
    This class is used to transfer author data between layers of the application.
    It contains the author's ID and associated Person object.
    """
    def __init__(self,id_author:int,person:Person):
        self.id_author = id_author
        self.person = person

    def __eq__(self, other):
        """
        Compares two AuthorDTO objects for equality based on their id_author.
        arguments:
            other (AuthorDTO): The other AuthorDTO object to compare with.
        """
        if not isinstance(other, AuthorDTO):
            return NotImplemented
        return self.id_author == other.id_author

    def __hash__(self):
        """
        Returns a hash value for the AuthorDTO object based on its id_author.
        This is used to allow AuthorDTO objects to be used as keys in dictionaries or added to sets.
        """
        return hash(self.id_author)
