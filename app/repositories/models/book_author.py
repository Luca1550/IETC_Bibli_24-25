class BookAuthor:
    """
    Model representing the relationship between a book and its author.
    This class is used to link a book identified by its ISBN with an author identified by their ID.
    """
    def __init__(self,isbn:str,id_author:int):
        """
        Initializes a BookAuthor instance with the given ISBN and author ID.
        :param isbn: The ISBN of the book.
        :param id_author: The ID of the author.
        """
        self.isbn = isbn
        self.id_author = id_author