from repositories.models import Editor,Collection,Theme

class BookDTO:
    def __init__(self,editor:Editor,collection:Collection,theme:Theme):
        self.editor = editor
        self.collection = collection
        self.theme = theme