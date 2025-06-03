from repositories.models import Editor,Collection,Theme,Author
import datetime

class BookDTO:
    def __init__(self,isbn:str,title:str,date:datetime,price:float,
                editors:list[Editor],collection:Collection,
                themes:list[Theme],authors:list[Author]):
        self.isbn = isbn
        self.title = title
        self.date = date
        self.price = price
        self.editors = editors
        self.collection = collection
        self.themes = themes
        self.authors = authors