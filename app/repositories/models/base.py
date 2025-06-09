import itertools

class Base:
    """
    Base class providing a unique, auto-incrementing ID for its subclasses.

    Each subclass inheriting from Base will have its own independent ID counter,
    ensuring unique IDs within that specific class type.
    """
    _id_iter = itertools.count(1)

    def __init__(self, id: int|None = None):
        """
        Initializes a new instance with a unique ID.

        If an 'id' is provided, it will be used. Otherwise, a new unique ID
        is generated using the class's internal counter. If an ID is provided,
        the class's ID counter is updated to ensure future auto-generated IDs
        are higher than the provided one.

        Args:
            id (int | None): An optional unique identifier for the instance.
            If None, a new ID is generated.
        """
        self.id = id if id is not None else next(self._id_iter)
        if id:
            self.update_id_iter(id)

    @classmethod
    def update_id_iter(cls, start_at: int):
        """
        Updates the class's ID counter to ensure subsequent auto-generated IDs
        are greater than a specified value.

        This method is typically called when loading existing data (e.g., from a database or file)
        to prevent ID collisions with newly created instances. The counter is
        set to start incrementing from 'start_at + 1'.

        Args:
            start_at (int): The maximum existing ID found. The next auto-generated
        """
        cls._id_iter = itertools.count(start_at + 1)