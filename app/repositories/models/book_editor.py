class BookEditor:
    """
    Model representing the relationship between a book and its editor.
    This class is used to link a book identified by its ISBN with an editor identified by their ID.
    """
    def __init__(self,isbn:str,id_editor:int):
        """
        Initializes a BookEditor instance with the given ISBN and editor ID.
        :param isbn: The ISBN of the book.
        :param id_editor: The ID of the editor.
        """
        self.isbn = isbn
        self.id_editor = id_editor