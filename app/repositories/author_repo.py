from repositories.models import Author
from tools import JsonStorage
import pathlib

class AuthorRepo:
    PATH_AUTHOR_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "author.json"
    
    def __init__(self):
        self.author_json : list[Author] = JsonStorage.load_all(self.PATH_AUTHOR_JSON)
    
    def add_author(self,author:Author):
        self.author_json.append(author)
        JsonStorage.save_all(self.PATH_AUTHOR_JSON,self.author_json)