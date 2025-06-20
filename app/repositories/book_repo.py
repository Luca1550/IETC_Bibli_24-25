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
    
    book_json : list[Book] = JsonStorage.load_all(PATH_BOOK_JSON)
    def __init__(self):
        """
        Initializes the BookRepo instance.
        Loads existing books from the JSON file into the book_json attribute.
        """
    
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
        if isinstance (book, Book):
            self.book_json.append(book)
            self._save_all()
            return True
        return False
    
    def is_unique(self,attribute:str,value:object):
        """
        Checks if a book with a specific attribute and value is unique in the repository.
        arguments:
        - attribute: The attribute of the book to check (e.g., 'isbn', 'title').
        - value: The value of the attribute to check for uniqueness.
        returns:
        - True if no book with the specified attribute and value exists, False otherwise.
        """
        return not any (getattr(isbn,attribute,None)== value for isbn in self.book_json)

    def get_all(self):
        """
        Returns all books in the repository.
        returns:
        - A list of Book objects.
        """
        return self.book_json
    
    def get_by_isbn(self,isbn:str):
        """
        Retrieves a book by its ISBN.
        arguments:
        - isbn: The ISBN of the book to retrieve.
        returns:
        - The Book object with the specified ISBN, or None if not found.
        """
        for book in self.book_json:
            if book.isbn == isbn:
                return book
        return None
    
    def update_book(self,book:Book) -> bool:
        if isinstance(book, Book):
            self.book_json[self.book_json.index(book)] = book
            self._save_all()
            return True
        return False

    def delete_book(self,book:Book) -> bool : 
        """
        Deletes a book from the repository.
        arguments:
        - book: The Book object to be deleted.
        returns:
        - True if the book was deleted successfully, False otherwise.
        """
        if isinstance (book, Book):
            self.book_json.remove(book)
            self._save_all()
            return True
        return False