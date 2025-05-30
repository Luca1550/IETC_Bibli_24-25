from repositories.models import Editor,Collection,Theme,Author

class BookDTO:
    def __init__(self,editors:list[Editor],collection:Collection,themes:list[Theme],authors:list[Author]):
        self.editors = editors
        self.collection = collection
        self.themes = themes
        self.authors = authors