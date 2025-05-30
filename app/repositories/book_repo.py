from repositories.models import Book
from tools import JsonStorage
import pathlib

class BookRepo:
    """
    Repository for managing books.
    Provides methods to load, add, and save books.
    Attributes:
        PATH_BOOK_JSON (pathlib.Path): Path to the JSON file storing books.
    """
    PATH_BOOK_JSON = pathlib.Path(__file__).parent.parent.parent / "database" / "book.json"
    
    def __init__(self):
        """
        Initializes the BookRepo instance.
        Loads existing books from the JSON file into the book_json attribute.
        """
        self.book_json : list[Book] = JsonStorage.load_all(self.PATH_BOOK_JSON)
    
    def _save_all(self):
        """
        Saves all Person data to the JSON file.
        """
        JsonStorage.save_all(self.PATH_BOOK_JSON, self.book_json)
    
    def add_book(self,book:Book):
        """
        Adds a Book object to the repository and saves it to the JSON file.
        arguments:
        - book: Book object to be added.
        returns:
        - True if the book was added successfully, False otherwise.
        """
        if book:
            self.book_json.append(book)
            self._save_all()
            return True
        return False