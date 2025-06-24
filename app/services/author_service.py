from repositories import AuthorRepo, PersonRepo, BookAuthorRepo
from .models import AuthorDTO
from repositories.models import Author
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
    
    def add_author(self, first_name : str, last_name : str | None) -> Author | Exception:
        """
        Adds a new author to the system.
        arguments:
        - first_name: First name of the author.
        - last_name: Last name of the author.
        returns:
        - Returns an error message if there was an issue adding the author.
        - Raises an exception if the author already exists or if there is an error during the addition
        """
        try:
            self._check_author_value(first_name,last_name)
            self._check_author_is_unique(first_name,last_name)
            person = self.person_service.add_person(first_name, last_name, None, None, None, None, None)
            self.author_repo.add_author(Author(id=None,id_person=person.id))
        except Exception as e:
            raise Exception(f"🛑 error adding author: {e}")
        
    def update_author(self, id : int, first_name : str, last_name : str | None) -> Author | Exception:
        """
        Updates an existing author's details.
        arguments:
        - id: Unique identifier of the author to be updated.
        - first_name: New first name of the author.
        - last_name: New last name of the author.
        returns:
        - Returns an error message if there was an issue updating the author.
        """
        try:
            author = self.author_repo.get_by_id(id)
            if not author:
                raise Exception(f"Author with the given ID : {id} was not found.")
            person = self.person_service.get_by_id(author.id_person)
            if person:
                self.person_service.update_person(person.id, first_name, last_name, None, None, None, None, None)
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
        self.person_repo = PersonRepo()
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
    
    def _check_author_value(self,first_name:str,last_name:str):
        """
        Checks if the author values are valid."""
        if not first_name or len(first_name.strip())<1:
            raise Exception ("First name cannot be empty.")
        if not last_name or len(last_name.strip())<1:
            raise Exception ("Last name cannot be empty.")
        return True

    def _check_author_is_unique (self,first_name:str,last_name:str):
        """
        Checks if the author is unique in the system.
        """
        first_name = first_name.strip().lower()
        last_name = last_name.strip().lower()
        for author in self.author_repo.get_all():
            person = self.person_repo.get_by_id(author.id_person)
            if person and person.first_name.strip().lower() == first_name and person.last_name.strip().lower() == last_name:
                raise Exception(f"Author '{first_name} {last_name}' already exists.")