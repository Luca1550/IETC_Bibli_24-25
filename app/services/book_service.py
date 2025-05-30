from repositories import EditorRepo,CollectionRepo,ThemeRepo,AuthorRepo
from .models import BookDTO

class BookService:
    def __init__(self,editor_repo:EditorRepo,collection_repo:CollectionRepo,theme_repo:ThemeRepo,author_repo:AuthorRepo):
        self.editor_repo = editor_repo
        self.collection_repo = collection_repo
        self.theme_repo = theme_repo
        self.author_repo = author_repo