from repositories import AuthorRepo, PersonRepo, BookAuthorRepo
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
        self.book_author_repo = BookAuthorRepo()
    
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
            raise Exception(f"🛑 error adding author: {e}")
    
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
    
    def delete_author(self,id : int):
        """
        Deletes an author by their ID.

        Arguments:
        - id: The unique identifier of the author.

        Returns:
        - True if the deletion was successful.
        - Raises an exception if the author is referenced elsewhere or not found.
        """
        try:    
            if self.book_author_repo.exist("id_author", id):
                raise Exception("Cannot delete, already used womewhere else.")
            if self.author_repo.delete_author(id):
                return True
            raise Exception(f"Author ID: {id} not found")
        except Exception as e:
            raise Exception(f"🛑 error {e}")
