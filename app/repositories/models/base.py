class Base:
    """
    Base class providing a unique, auto-incrementing ID for its subclasses.

    Each subclass inheriting from Base will have its own independent ID counter,
    ensuring unique IDs within that specific class type.
    """

    def __init_subclass__(cls):
        """
        This method is called automatically when a subclass is created.
        It ensures that each new subclass gets its own independent ID counter,
        starting from 1.
        """
        super().__init_subclass__()
        cls._next_id = 1

    def __init__(self, id: int | None = None):
        """
        Initializes a new instance with a unique ID specific to its class.

        If an 'id' is provided, it will be used. Otherwise, a new unique ID
        is generated using the class's internal counter. If an ID is provided
        and it's greater than or equal to the current next available ID,
        the class's ID counter is updated to ensure future auto-generated IDs
        are higher than the provided one.

        Args:
            id (int | None): An optional unique identifier for the instance.
            If None, a new ID is generated.
        """
        if id is not None:
            self.id = id
            self.__class__._next_id = self.id + 1
        else:
            self.id = self.__class__._next_id
            self.__class__._next_id += 1
