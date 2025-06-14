from repositories.models import BookEditor,Editor
from repositories import EditorRepo
from tools import JsonStorage
import pathlib

class BookEditorRepo:
    """
    Repository for managing the relationship between books and editors.
    This class provides methods to add book-editor relationships and retrieve editors by book ISBN.
    """
    PATH_BOOK_EDITOR_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "book_editor.json"
    
    def __init__(self):
        """
        Initializes the BookEditorRepo instance.
        Loads all book-editor relationships from the JSON file.
        """
        self.book_editor_json : list[BookEditor] = JsonStorage.load_all(self.PATH_BOOK_EDITOR_JSON)
        self._editor_repo : EditorRepo = EditorRepo()
    
    def _save_all(self):
        """
        Saves all book-editor relationships to the JSON file.
        This method is called after adding a new book-editor relationship.
        """
        JsonStorage.save_all(self.PATH_BOOK_EDITOR_JSON, self.book_editor_json)
    
    def add_book_editor(self,isbn:str,id_editor:int):
        """
        Adds a new book-editor relationship.
        :param isbn: ISBN of the book.
        :param id_editor: ID of the editor.
        This method creates a new BookEditor instance and appends it to the list of book-editor relationships.
        It then saves the updated list to the JSON file.
        """
        self.book_editor_json.append(BookEditor(isbn=isbn,id_editor=id_editor))
        self._save_all()

    def get_all(self):
        """
        Retrieves all book-editor relationships.
        :return: A list of all BookEditor instances.
        """
        return self.book_editor_json
    
    def get_editors_by_isbn(self,isbn:str):
        """
        Retrieves all editors associated with a given book ISBN.
        :param isbn: ISBN of the book.
        :return: A list of Editor instances associated with the given ISBN.
        This method filters the book-editor relationships to find those that match the given ISBN,
        and then retrieves the corresponding Editor instances using the EditorRepo.
        """
        lst_editor : list[Editor] = []
        for book_editor in self.book_editor_json:
            if book_editor.isbn == isbn:
                lst_editor.append(self._editor_repo.get_by_id(book_editor.id_editor))
        return lst_editor
    
    def delete_book_editor(self,isbn:str):
        """
        Deletes a book-editor relationship based on the given ISBN.
        :param isbn: ISBN of the book.
        This method iterates through the list of book-editor relationships and removes the one that matches the given ISBN.
        """
        for book_editor in self.book_editor_json:
            if book_editor.isbn == isbn:
                self.book_editor_json.remove(book_editor)
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
        return any(getattr(editor, attribute, None) == value for editor in self.book_editor_json)