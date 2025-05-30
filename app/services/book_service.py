from repositories import BookRepo,BookThemeRepo,BookEditorRepo,BookAuthorRepo,CollectionRepo
from repositories.models import Book,Theme,Author,Editor,Collection
from .models import BookDTO,AuthorDTO
import datetime

class BookService:
    def __init__(self):
        self._book_repo = BookRepo()
        self._book_theme_repo = BookThemeRepo()
        self._book_editor_repo = BookEditorRepo()
        self._book_author_repo = BookAuthorRepo()
        self._collection_repo = CollectionRepo()
    
    def add_book(self,isbn:str,title:str,date:datetime,price:float,collection:Collection,authors:list[AuthorDTO],themes:list[Theme],editors:list[Editor]):
        try:
            if self._book_repo.is_unique("isbn",isbn):
                self._book_repo.add_book(Book(
                    isbn=isbn,
                    title=title,
                    date=date,
                    price=price,
                    id_collection = collection.id
                ))
            else:
                raise ValueError("Cet ISBN existe déjà.")
            if authors:
                for author in authors:
                    self._book_author_repo.add_book_author(isbn,author.id_author)
            if themes:
                for theme in themes:
                    self._book_theme_repo.add_book_theme(isbn,theme.id)
            if editors:
                for editor in editors:
                    self._book_editor_repo.add_book_editor(isbn,editor.id)
        except ValueError as e:
            return f"Erreur : {e}"