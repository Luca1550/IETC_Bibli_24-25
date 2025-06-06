class BookTheme:
    """
    Model representing the relationship between a book and a theme.
    """
    def __init__(self,isbn:str,id_theme:int):
        """
        Initializes a BookTheme instance.
        :param isbn: ISBN of the book.
        :param id_theme: ID of the theme.
        """
        self.isbn = isbn
        self.id_theme = id_theme