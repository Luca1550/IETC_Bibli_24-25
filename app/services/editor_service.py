from repositories import EditorRepo

class EditorService :
    """
    Service class for managing editors.
    This class provides methods to add, remove, and list editors.
    """
    def __init__(self):
        """
        Initializes the EditorService with a EditorRepo instance.
        """
        self.editor_repo = EditorRepo()
        
    def add_editor(self,name):
        """
        Adds a new editor with the given name.
        :param name: The name of the editor to add.
        :return: None
        """
        try:
            self.editor_repo.add_editor(name)
        except:
            print(f"Error adding editor: {name}")
            return f"Error adding editor: {name}"