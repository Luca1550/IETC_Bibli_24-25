from repositories.models import BookAuthor,Author
from repositories import AuthorRepo
from tools import JsonStorage
import pathlib

class BookAuthorRepo:
    """
    Repository for managing the relationship between books and authors.
    This class provides methods to add book-author relationships and retrieve authors by book ISBN.
    """
    PATH_BOOK_AUTHOR_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "book_author.json"
    
    book_author_json : list[BookAuthor] = JsonStorage.load_all(PATH_BOOK_AUTHOR_JSON)
    def __init__(self):
        """
        Initializes the BookAuthorRepo instance.
        Loads all book-author relationships from the JSON file.
        """
        self._author_repo : AuthorRepo = AuthorRepo()
    
    def _save_all(self):
        """
        Saves all book-author relationships to the JSON file.
        This method is called after adding a new book-author relationship.
        """
        JsonStorage.save_all(self.PATH_BOOK_AUTHOR_JSON,self.book_author_json)
    
    def add_book_author(self,isbn:str,id_author:int):
        """
        Adds a new book-author relationship.
        :param isbn: ISBN of the book.
        :param id_author: ID of the author.
        This method creates a new BookAuthor instance and appends it to the list of book-author relationships.
        It then saves the updated list to the JSON file.
        """
        self.book_author_json.append(BookAuthor(isbn=isbn,id_author=id_author))
        self._save_all()
    
    def get_all(self):
        """
        Retrieves all book-author relationships.
        :return: A list of all BookAuthor instances.
        """
        return self.book_author_json
    
    def get_author_by_isbn(self,isbn:str):
        """
        Retrieves all authors associated with a given book ISBN.
        :param isbn: ISBN of the book.
        :return: A list of Author instances associated with the given ISBN.
        This method filters the book-author relationships to find those that match the given ISBN,
        and then retrieves the corresponding Author instances using the AuthorRepo.
        """
        lst_author : list[Author] = []
        for book_author in self.book_author_json:
            if book_author.isbn == isbn:
                lst_author.append(self._author_repo.get_by_id(book_author.id_author))
        return lst_author
    
    def delete_book_author(self,isbn:str):
        """
        Deletes a book-author relationship by ISBN.
        :param isbn: ISBN of the book.
        This method iterates through the list of book-author relationships and removes any that match the given ISBN.
        It then saves the updated list to the JSON file.
        """
        for book_author in self.book_author_json:
            if book_author.isbn == isbn:
                self.book_author_json.remove(book_author)
        self._save_all()

    def exist(self, attribute : str, value : object) -> bool:
        """
        Checks if a given attribute of an object is unique in the repository.
        arguments:
        - attribute: The attribute to check for uniqueness.
        - value: The value to check against the specified attribute.
        returns:
        - True if the value is unique, False if it already exists in the repository.
        """
        return any(getattr(author, attribute, None) == value for author in self.book_author_json)