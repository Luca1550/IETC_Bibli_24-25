from repositories import EditorRepo, BookEditorRepo

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
        self.book_editor_repo = BookEditorRepo()
        
    def add_editor(self,name):
        """
        Adds a new editor with the given name.
        arguments:
        - name: The name of the editor to add.
        returns:
        - True if the editor was added successfully.
        - Raises an exception if the editor already exists or if there is an error during the addition.
        """
        try:
            if not self.editor_repo.is_unique("name",name):
                raise Exception("This editor already exists")
            return self.editor_repo.add_editor(name)
        except Exception as e:
            raise Exception(f"error adding editor: {name} - {e}")

    def get_by_name(self,name):
        """
        Retrieves a editor by its name.
        :param name: The name of the editor to retrieve.
        :return: The editor object if found, None otherwise.
        """
        editor = self.editor_repo.get_by_name(name)
        if editor:
            return editor
        else : 
            return "Editor not found"
    
    def get_by_id(self,id):
        """
        Retrieves a editor by its ID.
        :param id: The ID of the editor to retrieve.
        :return: The editor object if found, None otherwise.
        """
        editor = self.editor_repo.get_by_id(id)
        if editor:
            return editor
        else : 
            return "Editor not found"
    
    def get_all(self):
        """
        Retrieves all editors.
        :return: A list of all editors.
        """
        return self.editor_repo.get_all()
    
    def update_editor_by_id(self,id:int,name:str):
        """
        Updates the name of a editor by its ID.
        :param id: The ID of the editor to update.
        :param name: The new name for the editor.
        :return: A message indicating the result of the update.
        """
        if self.editor_repo.update_editor_by_id(id,name):
            return f"Editor with ID {id} updated : {name}"
        else:
            return f"Editor with ID {id} not found"
        
    def update_editor_by_name(self,name:str,new_name:str):
        """
        Updates the name of a editor by its current name.
        :param name: The current name of the editor to update.
        :param new_name: The new name for the editor.
        :return: A message indicating the result of the update.
        """
        if self.editor_repo.update_editor_by_name(name,new_name):
            return f"Editor {name} updated en {new_name}"
        else:
            return f"Editor {name} not found"
    
    def delete_editor(self,id : int):
        """
        Deletes an editor by their ID.

        Arguments:
        - id: The unique identifier of the editor.

        Returns:
        - True if the deletion was successful.
        - Raises an exception if the editor is referenced elsewhere or not found.
        """
        try:    
            if self.book_editor_repo.exist("id_editor", id):
                raise Exception("Cannot delete, already used womehere else.")
            editor = self.editor_repo.get_by_id(id)
            if self.editor_repo.delete_editor(editor):
                return True
            raise Exception(f"Editor ID: {id} not found")
        except Exception as e:
            raise Exception(f"🛑 error {e}")