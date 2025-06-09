from repositories.models import Editor,Collection,Theme
from services.models import AuthorDTO
import datetime

class BookDTO:
    """
    Data Transfer Object for Book.
    This class is used to transfer book data between different layers of the application.
    """
    def __init__(self,isbn:str,title:str,date:datetime,price:float,
                editors:list[Editor],collection:Collection,
                themes:list[Theme],authors:list[AuthorDTO]):
        """
        Initializes a BookDTO instance with the provided parameters.
        :param isbn: ISBN of the book.
        :param title: Title of the book.
        :param
        date: Publication date of the book.
        :param price: Price of the book.
        :param editors: List of editors associated with the book.
        :param collection: Collection to which the book belongs.
        :param themes: List of themes associated with the book.
        :param authors: List of authors associated with the book.
        """
        self.isbn = isbn
        self.title = title
        self.date = date
        self.price = price
        self.editors = editors
        self.collection = collection
        self.themes = themes
        self.authors = authors

    def __eq__(self, other):
        """
        Compares two BookDTO objects for equality based on their ID.
        arguments:
            other (BookDTO): The other BookDTO object to compare with.
        """
        if isinstance(other, BookDTO):
            return self.isbn == other.isbn

    def __hash__(self):
        """
        Returns a hash value for the BookDTO object based on its ID.
        """
        return hash(self.isbn)