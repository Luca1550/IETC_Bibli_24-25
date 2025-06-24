from enum import Enum

class Status(Enum):
    """
    Enum representing the status of a book in a library system.
    """
    AVAILABLE = 1
    BORROWED = 2
    RESERVED = 3