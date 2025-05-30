from repositories.models import BookAuthor,Author
from repositories import AuthorRepo
from tools import JsonStorage
import pathlib

class BookAuthorRepo:
    PATH_BOOK_AUTHOR_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "book_author.json"
    
    def __init__(self):
        self.book_author_json : list[BookAuthor] = JsonStorage.load_all(self.PATH_BOOK_AUTHOR_JSON)
        self._author_repo : AuthorRepo = AuthorRepo()
    
    def _save_all(self):
        JsonStorage.save_all(self.PATH_BOOK_AUTHOR_JSON,self.book_author_json)
    
    def add_book_author(self,isbn:str,id_author:int):
        self.book_author_json.append(BookAuthor(isbn=isbn,id_author=id_author))
        self._save_all()
    
    def get_all(self):
        return self.book_author_json
    
    def get_author_by_isbn(self,isbn:str):
        lst_author : list[Author] = []
        for book_author in self.book_author_json:
            if book_author.isbn == isbn:
                lst_author.append(self._author_repo.get_by_id(book_author.id_author))
        return lst_author