from repositories.models import BookEditor,Editor
from repositories import EditorRepo
from tools import JsonStorage
import pathlib

class BookEditorRepo:
    PATH_BOOK_EDITOR_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "book_editor.json"
    
    def __init__(self):
        self.book_editor_json : list[BookEditor] = JsonStorage.load_all(self.PATH_BOOK_EDITOR_JSON)
        self._editor_repo : EditorRepo = EditorRepo()
    
    def _save_all(self):
        JsonStorage.save_all(self.PATH_BOOK_EDITOR_JSON, self.book_editor_json)
    
    def add_book_editor(self,isbn:str,id_editor:int):
        self.book_editor_json.append(BookEditor(isbn=isbn,id_editor=id_editor))
        self._save_all()

    def get_all(self):
        return self.book_editor_json
    
    def get_editors_by_isbn(self,isbn:str):
        lst_editor : list[Editor] = []
        for book_editor in self.book_editor_json:
            if book_editor.isbn == isbn:
                lst_editor.append(self._editor_repo.get_by_id(book_editor.id_editor))
        return lst_editor