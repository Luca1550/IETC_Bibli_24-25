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