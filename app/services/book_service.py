from repositories import BookRepo,BookThemeRepo,BookEditorRepo,BookAuthorRepo,CollectionRepo
from repositories.models import Book,Theme,Author,Editor
from .models import BookDTO
import datetime

class BookService:
    def __init__(self):
        self._book_repo = BookRepo()
        self._book_theme_repo = BookThemeRepo()
        self._book_editor_repo = BookEditorRepo()
        self._book_author_repo = BookAuthorRepo()
        self._collection_repo = CollectionRepo()
    