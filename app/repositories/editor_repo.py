from repositories.models import Editor
from tools import JsonStorage
import pathlib

class EditorRepo:
    """
    Repository for managing editor.
    Provides methods to load, add, and save editor.
    Attributes:
        PATH_EDITOR_JSON (pathlib.Path): Path to the JSON file storing editor.
    """
    PATH_EDITOR_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "editor.json"
    
    def __init__(self):
        """
        Initializes the EditorRepo instance.
        Loads existing editor from the JSON file into the editor_json attribute.
        """
        self.editor_json : list[Editor] = JsonStorage.load_all(self.PATH_EDITOR_JSON)
    
    def add_editor(self,name:str):
        """
        Adds a new editor with the specified name to the repository.
        The new editor is assigned a unique ID based on the current maximum ID in the repository.
        Args:
            name (str): The name of the editor to be added.
        """
        self.editor_json.append(Editor(id = None,name = name))
        JsonStorage.save_all(self.PATH_EDITOR_JSON,self.editor_json)
        return True
    
    def get_by_name(self,name:str):
        """
        Retrieves a editor by its name from the repository.
        Args:
            name (str): The name of the editor to be retrieved.
        Returns:
            Editor: The Editor object if found, None otherwise.
        """
        for editor in self.editor_json:
            if editor.name == name:
                return editor
        return None
        
    def get_by_id (self,id:int):
        """
        Retrieves a editor by its ID from the repository.
        Args:
            id (int): The ID of the editor to be retrieved.
        Returns:
            Editor: The editor object if found, None otherwise.
        """
        for editor in self.editor_json:
            if editor.id == id:
                return editor
        return None
        
    def get_all(self):
        """
        Retrieves all editors from the repository.
        Returns:
            list[Editor]: A list of all editor objects.
        """
        return self.editor_json
    
    def update_editor_by_id(self,id:int,name:str):
        """
        Updates the name of a editor by its ID.
        Args:
            id (int): The ID of the editor to be updated.
            name (str): The new name for the editor.
        Returns:
            bool: True if the editor was found and updated, False otherwise.
        """
        for editor in self.editor_json:
            if editor.id == id:
                editor.name = name
                JsonStorage.save_all(self.PATH_EDITOR_JSON, self.editor_json)
                return True
        return False
    
    def update_editor_by_name(self,name:str,new_name:str):
        """
        Updates the name of a editor by its current name.
        Args:
            name (str): The current name of the editor to be updated.
            new_name (str): The new name for the editor.
        Returns:
            bool: True if the editor was found and updated, False otherwise.
        """
        for editor in self.editor_json:
            if editor.name == name:
                editor.name = new_name
                JsonStorage.save_all(self.PATH_EDITOR_JSON, self.editor_json)
                return True
        return False
    
    def delete_editor(self, editor : Editor):
        """
        Deletes a editor from the repository.
        arguments:
        - editor: The editor object to be deleted.
        returns:
        - True if the deletion was successful, False otherwise.
        """
        if isinstance(editor, Editor):
            self.editor_json.remove(editor)
            JsonStorage.save_all(self.PATH_EDITOR_JSON, self.editor_json)
            return True
        return False
    
    def is_unique(self, attribute : str, value : object) -> bool:
        """
        Checks if a given attribute of an object is unique in the repository.
        arguments:
        - attribute: The attribute to check for uniqueness.
        - value: The value to check against the specified attribute.
        returns:
        - True if the value is unique, False if it already exists in the repository.
        """
        return not any(getattr(editor, attribute, None) == value for editor in self.editor_json)