from repositories.models import Theme
from tools import JsonStorage
import pathlib

class ThemeRepo:
    """
    Repository for managing themes.
    Provides methods to load, add, and save themes.
    Attributes:
        PATH_THEME_JSON (pathlib.Path): Path to the JSON file storing themes.
    """
    PATH_THEME_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "theme.json"
    
    def __init__(self):
        """
        Initializes the ThemeRepo instance.
        Loads existing themes from the JSON file into the theme_json attribute.
        """
        self.theme_json : list[Theme] = JsonStorage.load_all(self.PATH_THEME_JSON)
        
    def add_theme(self,name:str):
        """
        Adds a new theme with the specified name to the repository.
        The new theme is assigned a unique ID based on the current maximum ID in the repository.
        Args:
            name (str): The name of the theme to be added.
        """
        self.theme_json.append(Theme(id = None,name = name))
        JsonStorage.save_all(self.PATH_THEME_JSON,self.theme_json)
        
    def delete_theme(self,name:str):
        """
        Deletes a theme by its name from the repository.
        Args:
            name (str): The name of the theme to be deleted.
        Returns:
            bool: True if the theme was found and deleted, False otherwise.
        """
        for theme in self.theme_json:
            if theme.name == name:
                self.theme_json.remove(theme)
                JsonStorage.save_all(self.PATH_THEME_JSON, self.theme_json)
                return True
        return False

    def get_by_theme (self,name:str):
        """
        Retrieves a theme by its name from the repository.
        Args:
            name (str): The name of the theme to be retrieved.
        Returns:
            Theme: The theme object if found, None otherwise.
        """
        for theme in self.theme_json:
            if theme.name == name:
                return theme
        return None
        
    def get_by_id (self,id:int):
        for theme in self.theme_json:
            if theme.id == id:
                return theme
        return None
        
    def get_all(self):
        return self.theme_json