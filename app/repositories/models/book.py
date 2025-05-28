import datetime

class Book:
    """
    Represents a book with its ISBN, title, publication date, and price.
    Attributes:
        isbn (str): International Standard Book Number, a unique identifier for the book.
        title (str): Title of the book.
        date (datetime): Publication date of the book.
        price (float): Price of the book.
    """
    def __init__(self,isbn:str,title:str,date:datetime,price:float):
        self.isbn = isbn
        self.title = title
        self.date = date
        self.price = price
        