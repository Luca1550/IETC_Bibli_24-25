from repositories.models import  Person

class AuthorDTO:
    def __init__(self,id_author:int,person:Person):
        self.id_author = id_author
        self.person = person