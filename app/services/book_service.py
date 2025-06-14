from repositories import BookRepo,BookThemeRepo,BookEditorRepo,BookAuthorRepo,CollectionRepo
from repositories.models import Book,Theme,Author,Editor,Collection
from .models import BookDTO,AuthorDTO
from services import AuthorService, ExemplarService
import datetime

class BookService:
    
    def __init__(self):
        """
        Initializes the BookService with repositories for books, themes, editors, authors, and collections.
        This constructor sets up the necessary repositories to manage book-related data, allowing for operations such as adding books and retrieving book details.
        """
        self._book_repo = BookRepo()
        self._book_theme_repo = BookThemeRepo()
        self._book_editor_repo = BookEditorRepo()
        self._book_author_repo = BookAuthorRepo()
        self._collection_repo = CollectionRepo()
        self._author_service = AuthorService()
        self._exemplar_service = ExemplarService()      
    
    def add_book(self,isbn:str,title:str,date:datetime,price:float,collection:Collection,authors:list[AuthorDTO],themes:list[Theme],editors:list[Editor]):
        """
        Adds a new book to the repository with its associated collection, authors, themes, and editors.
        :param isbn: ISBN of the book.
        :param title: Title of the book.
        :param date: Publication date of the book.
        :param price: Price of the book.
        :param collection: Collection to which the book belongs.
        :param authors: List of AuthorDTO objects representing the authors of the book.
        :param themes: List of Theme objects representing the themes of the book.
        :param editors: List of Editor objects representing the editors of the book.
        :return: None or an error message if the book already exists.
        This method checks if the ISBN is unique before adding the book to the repository. If the ISBN already exists, it raises a ValueError.
        """
        try:
            if self._book_repo.is_unique("isbn",isbn):
                if self._check_book_value(isbn,title,date,price,authors,themes,editors):
                    self._book_repo.add_book(Book(
                        isbn=isbn,
                        title=title,
                        date=date,
                        price=price,
                        id_collection = collection.id if collection is not None else 0
                    ))
                else:
                    raise Exception("Values are wrong.")
            else:
                raise Exception("This ISBN already exists.")
            if authors:
                for author in authors:
                    self._book_author_repo.add_book_author(isbn,author.id_author)
            if themes:
                for theme in themes:
                    self._book_theme_repo.add_book_theme(isbn,theme.id)
            if editors:
                for editor in editors:
                    self._book_editor_repo.add_book_editor(isbn,editor.id)
            
            return self.get_by_isbn(isbn)
        except Exception as e:
            raise Exception(f"🛑 Error {e}")
    
    def get_all(self):
        """
        Returns a list of all books with their associated collections, authors, editors, and themes.
        :return: List of BookDTO objects containing book details along with associated collections, authors, editors, and themes.
        
        This method retrieves all books from the repository, along with their associated collections, authors, editors, and themes.
        Each book is represented as a BookDTO object, which includes the book's ISBN, title, date, price, and lists of associated authors, editors, themes, and collection.
        """
        books = self._book_repo.get_all()
        result : list[BookDTO] = []
        
        for book in books:
            collection = self._collection_repo.get_by_id(book.id_collection)
            
            authors = self._book_author_repo.get_author_by_isbn(book.isbn)
            author_dto:list[AuthorDTO] = []
            for author in authors:
                author_dto.append(self._author_service.get_by_id(author.id))
            editors = self._book_editor_repo.get_editors_by_isbn(book.isbn)
            themes = self._book_theme_repo.get_themes_by_isbn(book.isbn)
            
            book_dto = BookDTO(
                isbn=book.isbn,
                title=book.title,
                date=book.date,
                price=book.price,
                editors=editors,
                themes=themes,
                authors=author_dto,
                collection=collection
            )
            
            result.append(book_dto)
            
        return result
    
    def get_by_isbn(self,isbn):
        try:
            books_dto = self.get_all()
            for book in books_dto : 
                if book.isbn == isbn:
                    return book
            else:
                raise Exception(f"Book with the given ID : {isbn} was not found.")
        except Exception as e:
            return f"🛑 Error [{e}]"
        
    def update_by_parameter(self,isbn:str,title:str,date:datetime,price:float,collection:Collection,authors:list[AuthorDTO],themes:list[Theme],editors:list[Editor]):
        try:
            book:Book = self._book_repo.get_by_isbn(isbn)
            book_dto: BookDTO = self.get_by_isbn(isbn)
            if not isinstance(book,Book):
                raise Exception(f"Book with ISBN: {isbn} was not found.")
            if self._check_book_value(isbn=isbn,title=title,date=date,price=price,authors=authors,themes=themes,editors=editors):
                if title is not None:
                    book.title = title
                if date is not None:
                    book.date = date
                if price is not None:
                    book.price = price
                if collection is None:
                    book.id_collection = -1
                else:
                    book.id_collection = collection.id
                
                
                self._book_repo.update_book(book)
                
                if authors is not None:
                    for i in enumerate(book_dto.authors):
                        self._book_author_repo.delete_book_author(isbn)
                    for author in authors:
                        self._book_author_repo.add_book_author(isbn, author.id_author)
                
                if themes is not None:
                    for i in enumerate(book_dto.themes):
                        self._book_theme_repo.delete_book_theme(isbn)
                    for theme in themes:
                        self._book_theme_repo.add_book_theme(isbn, theme.id)
                
                if editors is not None:
                    for i in enumerate(book_dto.editors):
                        self._book_editor_repo.delete_book_editor(isbn)
                    for editor in editors:
                        self._book_editor_repo.add_book_editor(isbn, editor.id)
                    
        except Exception as e:
            raise Exception(f"🛑 Error {e}")
        
    def delete_book(self,isbn):
        """
        Deletes a book by its ISBN along with its associated authors, editors, and themes.
        :param isbn: ISBN of the book to be deleted.
        :return: True if the book was deleted successfully, or an error message if an exception occurred.
        This method retrieves the book by its ISBN, deletes all associated authors, editors, and themes, and then deletes the book itself.
        If the book is not found, it raises an exception.
        """
        try:
            book_dto = self.get_by_isbn(isbn)
            if not self._exemplar_service.check_all_status_by_isbn(book_dto.isbn):
                raise Exception("You cannot delete this book as all exemplars must be available before the deletion")
            book_exemplars = self._exemplar_service.get_all_by_isbn(book_dto.isbn)
            if book_exemplars:
                for exemplar in book_exemplars:
                    self._exemplar_service.delete_exemplar(exemplar.id)
            book = self._book_repo.get_by_isbn(isbn)
            if isinstance(book_dto, BookDTO):
                for i in enumerate(book_dto.authors):
                    self._book_author_repo.delete_book_author(book_dto.isbn)
                for i in enumerate(book_dto.editors):
                    self._book_editor_repo.delete_book_editor(book_dto.isbn)
                for i in enumerate(book_dto.themes):
                    self._book_theme_repo.delete_book_theme(book_dto.isbn) 
                self._book_repo.delete_book(book)
                return True
            raise Exception(book)
        except Exception as e:
            print(e)
            raise Exception(f"🛑 Error [{e}]")
        
    def _check_book_value(self,isbn:str,title:str,date:datetime,price:float,authors:list[AuthorDTO],themes:list[Theme],editors:list[Editor]):
        if not isbn or len(isbn)!=13 or not isbn.isnumeric():
            raise Exception("Invalid ISBN. must be exactly 13 characters long.")
        if not title.strip():
            raise Exception("Title cannot be empty.")
        if not date:
            raise Exception ("Must include a valid date.")
        if not authors:
            raise Exception("At least one author is required.")
        if not editors:
            raise Exception("At least one editor is required.")
        if not themes:
            raise Exception("At least on theme is required.")
        try:
            float(price)
        except:
            raise Exception("Price must be numeric")
        if not float(price)>0.00:
            raise Exception("Books aren't free.")
        return True