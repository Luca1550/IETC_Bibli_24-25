from repositories import AuthorRepo, PersonRepo
from .models import AuthorDTO
from repositories.models import Person, Author

class AuthorService:
    
    def __init__(self):
        self.author_repo = AuthorRepo()
        self.person_repo = PersonRepo()
    
    def add_author(self,person:Person):
        try:
            if self.person_repo.add_person(person):
                print(person.__dict__)
                self.author_repo.add_author(person.id)
        except:
            return f"Error adding author: {person}"