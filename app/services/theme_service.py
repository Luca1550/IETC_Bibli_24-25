from repositories import ThemeRepo

class ThemeService :
    """
    Service class for managing themes.
    This class provides methods to add, remove, and list themes.
    """
    def __init__(self):
        """
        Initializes the ThemeService with a ThemeRepo instance.
        """
        self.theme_repo = ThemeRepo()
        
    def add_theme(self,name):
        """
        Adds a new theme with the given name.
        :param name: The name of the theme to add.
        :return: None
        """
        try:
            self.theme_repo.add_theme(name)
        except:
            print(f"Error adding theme: {name}")
            return f"Error adding theme: {name}"
        
    def delete_theme(self,name):
        if self.theme_repo.delete_theme(name):
            print(f"Le theme : {name} a été supprimé")
            return f"Le theme : {name} a été supprimé"
        else:
            print(f"Le theme : {name} n'existe pas")
            return f"Le theme : {name} n'existe pas"