from repositories.models import BookTheme,Theme
from repositories import ThemeRepo
from tools import JsonStorage
import pathlib

class BookThemeRepo:
    PATH_BOOK_THEME_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "book_theme.json"
    
    def __init__(self):
        self.book_theme_json : list[BookTheme] = JsonStorage.load_all(self.PATH_BOOK_THEME_JSON)
        self._theme_repo : ThemeRepo = ThemeRepo()
    
    def _save_all(self):
        JsonStorage.save_all(self.PATH_BOOK_THEME_JSON, self.book_theme_json)
    
    def add_book_theme(self,isbn:str,id_theme:int):
        self.book_theme_json.append(BookTheme(isbn=isbn,id_theme=id_theme))
        self._save_all()

    def get_all(self):
        return self.book_theme_json
    
    def get_themes_by_isbn(self,isbn:str):
        lst_theme : list[Theme] = []
        for book_theme in self.book_theme_json:
            if book_theme.isbn == isbn:
                lst_theme.append(self._theme_repo.get_by_id(book_theme.id_theme))
        return lst_theme