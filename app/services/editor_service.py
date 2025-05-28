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
            return f"Error adding editor: {name}"
    
    def get_by_editor(self,name):
        """
        Retrieves a editor by its name.
        :param name: The name of the editor to retrieve.
        :return: The editor object if found, None otherwise.
        """
        editor = self.editor_repo.get_by_editor(name)
        if editor:
            return f"Editor : {editor.name}"
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
            return f"Editor : {editor.name}"
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
    
    def delete_editor(self,name):
        """
        Deletes a editor with the given name.
        :param name: The name of the editor to delete.
        :return: A message indicating the result of the deletion.
        """
        if self.editor_repo.delete_editor(name):
            return f"Editor : {name} deleted"
        else:
            return f"Editor : {name} not found"