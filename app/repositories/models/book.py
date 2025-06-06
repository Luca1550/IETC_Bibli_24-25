import datetime

class Book:
    """
    Represents a book with its ISBN, title, publication date, and price.
    
    """
    def __init__(self,isbn:str,title:str,date:datetime,price:float,id_collection:int):
        """
        Initializes a Book instance with the given parameters.
        :param isbn: The ISBN of the book.
        :param title: The title of the book.
        :param
        date: The publication date of the book.
        :param price: The price of the book.
        :param id_collection: The ID of the collection to which the book belongs.
        """
        self.isbn = isbn
        self.title = title
        self.date = date
        self.price = price
        self.id_collection = id_collection