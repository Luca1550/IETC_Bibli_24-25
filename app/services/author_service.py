from repositories import AuthorRepo, PersonRepo
from .models import AuthorDTO
from repositories.models import Person, Author
from .person_service import PersonService

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
        self.person_service = PersonService()
    
    def add_author(self, first_name : str, last_name : str, national_number: str, email : str, street : str, cp : str, city : str) -> Author:
        """
        Adds a new author to the system.
        :param person: Person object containing the details of the author to be added.
        Using the PersonService to create a new person and then adding the author to the AuthorRepo.
        :return: A message indicating success or failure.
        """
        try:
            person = self.person_service.add_person(first_name=first_name, last_name=last_name, national_number=national_number, email=email, street=street, cp=cp, city=city)
            self.author_repo.add_author(Author(id=None,id_person=person.id))
        except Exception as e:
            return f"Error adding author: {e}"
    
    def get_by_id(self,id:int):
        """
        Retrieves an author by their unique identifier.
        :param id: Unique identifier of the author.
        :return: AuthorDTO containing author details or None if not found.
        """
        author = self.author_repo.get_by_id(id)
        person = self.person_repo.get_by_id(author.id_person)
        return AuthorDTO(id_author=author.id, person=person)
    
    def get_all(self):
        authors=self.author_repo.get_all()
        authors_dto = []
        for author in authors:
            authors_dto.append(
                AuthorDTO(
                    id_author=author.id,
                    person=self.person_repo.get_by_id(author.id_person)
                )
            )
        return authors_dto
    
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
