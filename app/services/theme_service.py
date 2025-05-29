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
            return f"Error adding theme: {name}"
        
    def delete_theme(self,name):
        """
        Deletes a theme with the given name.
        :param name: The name of the theme to delete.
        :return: A message indicating the result of the deletion.
        """
        if self.theme_repo.delete_theme(name):
            return f"Theme : {name} deleted"
        else:
            return f"Theme : {name} not found"
        
    def get_by_name(self,name):
        """
        Retrieves a theme by its name.
        :param name: The name of the theme to retrieve.
        :return: The theme object if found, None otherwise.
        """
        theme = self.theme_repo.get_by_name(name)
        if theme:
            return f"Theme : {theme.name}"
        else : 
            return "Theme not found"
    
    def get_by_id(self,id):
        """
        Retrieves a theme by its ID.
        :param id: The ID of the theme to retrieve.
        :return: The theme object if found, None otherwise.
        """
        theme = self.theme_repo.get_by_id(id)
        if theme:
            return f"Theme : {theme.name}"
        else : 
            return "Theme not found"
    
    def get_all(self):
        """
        Retrieves all themes.
        :return: A list of all theme objects.
        """
        return self.theme_repo.get_all()
    
    def update_theme_by_id(self,id:int,name:str):
        """
        Updates the name of a theme by its ID.
        :param id: The ID of the theme to update.
        :param name: The new name for the theme.
        :return: A message indicating the result of the update.
        """
        if self.theme_repo.update_theme_by_id(id,name):
            return f"Theme with ID {id} updated to {name}"
        else:
            return f"Theme with ID {id} not found"
        
    def update_theme_by_name(self,name:str,new_name:str):
        """
        Updates the name of a theme by its current name.
        :param name: The current name of the theme to update.
        :param new_name: The new name for the theme.
        :return: A message indicating the result of the update.
        """
        if self.theme_repo.update_theme_by_name(name,new_name):
            return f"Theme {name} updated to {new_name}"
        else:
            return f"Theme {name} not found"
