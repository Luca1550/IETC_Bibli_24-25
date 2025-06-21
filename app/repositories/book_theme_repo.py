from repositories.models import BookTheme,Theme
from repositories import ThemeRepo
from tools import JsonStorage
import pathlib

class BookThemeRepo:
    """
    Repository for managing the relationship between books and themes.
    This class provides methods to add book-theme relationships and retrieve themes by book ISBN.
    """
    PATH_BOOK_THEME_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "book_theme.json"
    
    book_theme_json : list[BookTheme] = JsonStorage.load_all(PATH_BOOK_THEME_JSON)
    def __init__(self):
        """
        Initializes the BookThemeRepo instance.
        Loads all book-theme relationships from the JSON file.
        """
        self._theme_repo : ThemeRepo = ThemeRepo()
    
    def _save_all(self):
        """
        Saves all book-theme relationships to the JSON file.
        This method is called after adding a new book-theme relationship.
        """
        JsonStorage.save_all(self.PATH_BOOK_THEME_JSON, self.book_theme_json)
    
    def add_book_theme(self,isbn:str,id_theme:int):
        """
        Adds a new book-theme relationship.
        :param isbn: ISBN of the book.
        :param id_theme: ID of the theme.
        This method creates a new BookTheme instance and appends it to the list of book-theme relationships.
        It then saves the updated list to the JSON file.
        """
        self.book_theme_json.append(BookTheme(isbn=isbn,id_theme=id_theme))
        self._save_all()

    def get_all(self):
        """
        Retrieves all book-theme relationships.
        :return: A list of all BookTheme instances.
        """
        return self.book_theme_json
    
    def get_themes_by_isbn(self,isbn:str):
        """
        Retrieves all themes associated with a given book ISBN.
        :param isbn: ISBN of the book.
        :return: A list of Theme instances associated with the given ISBN.
        This method filters the book-theme relationships to find those that match the given ISBN,
        and then retrieves the corresponding Theme instances using the ThemeRepo.
        """
        lst_theme : list[Theme] = []
        for book_theme in self.book_theme_json:
            if book_theme.isbn == isbn:
                lst_theme.append(self._theme_repo.get_by_id(book_theme.id_theme))
        return lst_theme
    
    def delete_book_theme(self,isbn:str):
        """
        Deletes a book-theme relationship by ISBN.
        :param isbn: ISBN of the book.
        This method iterates through the list of book-theme relationships and removes the one that matches the given ISBN."""
        for book_theme in self.book_theme_json:
            if book_theme.isbn == isbn:
                self.book_theme_json.remove(book_theme)
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
        return any(getattr(theme, attribute, None) == value for theme in self.book_theme_json)