from repositories import AuthorRepo, PersonRepo
from .models import AuthorDTO
from repositories.models import Person, Author

class AuthorService:
    """
    AuthorService is responsible for managing authors in the system.
    """
    def __init__(self):
        """
        It interacts with the AuthorRepo and PersonRepo to perform operations related to authors.
        """
        self.author_repo = AuthorRepo()
        self.person_repo = PersonRepo()
    
    def add_author(self,person:Person):
        """
        Adds a new author to the system.
        :param person: Person object containing the details of the author to be added.
        :return: A message indicating success or failure.
        """
        try:
            if self.person_repo.add_person(person):
                self.author_repo.add_author(Author(id=None,id_person=person.id))
        except:
            self.person_repo.delete_person(person.id)
            return f"Error adding author: {person}"
    
    def get_by_id(self,id:int):
        """
        Retrieves an author by their unique identifier.
        :param id: Unique identifier of the author.
        :return: AuthorDTO containing author details or None if not found.
        """
        author = self.author_repo.get_by_id(id)
        person = self.person_repo.get_by_id(author.id_person)

        return AuthorDTO(id_author=author.id, person=person)
    
    def delete_author(self,id):
        """
        Deletes an author with the given name.
        :param name: The name of the author to delete.
        :return: A message indicating the result of the deletion.
        """
        if self.author_repo.delete_author(id):
            return f"Author ID: {id} deleted"
        else:
            return f"Author ID: {id} not found"
