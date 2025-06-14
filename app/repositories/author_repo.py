from repositories.models import Author
from tools import JsonStorage
import pathlib

class AuthorRepo:
    """
    AuthorRepo is responsible for managing authors in the system.
    """
    PATH_AUTHOR_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "author.json"
    
    def __init__(self):
        """
        Initializes the AuthorRepo instance and loads authors from the JSON file.
        If the file does not exist, it initializes an empty list of authors.
        """
        self.author_json : list[Author] = JsonStorage.load_all(self.PATH_AUTHOR_JSON)
    
    def add_author(self,author:Author):
        """
        Adds a new author to the repository.
        :param author: Author object to be added.
        """
        self.author_json.append(author)
        JsonStorage.save_all(self.PATH_AUTHOR_JSON,self.author_json)
    
    def get_by_id(self,id:int):
        """
        Retrieves an author by their unique identifier.
        :param id: Unique identifier of the author.
        :return: Author object if found, otherwise None.
        """
        for author in self.author_json:
            if author.id == id:
                return author
        return None
    
    def get_all(self):
        return self.author_json
    
    def delete_author(self,id:str):
        """
        Deletes a author by its name from the repository.
        Args:
            name (str): The name of the author to be deleted.
        Returns:
            bool: True if the author was found and deleted, False otherwise.
            
            WE DICIDED THAT DELETING AN AUTHOR WOULD NOT DELETE THE PERSON.
            PLEASE DON'T COMMENT ON THAT DECISION.
            WE KNOW THIS IS A LIABILITY.
            THANKS,
            LUCA.
        """
        for author in self.author_json:
            if author.id == id:
                self.author_json.remove(author)
                JsonStorage.save_all(self.PATH_AUTHOR_JSON, self.author_json)
                return True
        return False