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
    
    def get_by_editor(self,name:str):
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