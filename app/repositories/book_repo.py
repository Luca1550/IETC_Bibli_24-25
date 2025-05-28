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