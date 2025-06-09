from .base import Base

class Login(Base):
    """
    Represents a login with a unique ID, worker ID, username, and password.
    Inherits from Base to ensure each login has a unique identifier.
    """
    def __init__(self, id: int | None, worker_id: int | None, username: str, password: str):
        """
        Initializes a new Login instance with a unique ID, worker ID, username, and password.
        If an ID is provided, it will be used; otherwise, a new unique ID is generated.

        Args:
            id (int | None): Unique identifier for the login. If None, a new ID is generated.
            worker_id (int | None): Unique identifier for the associated worker. If None, a new ID is generated.
            username (str): Username for the login.
            password (str): Password for the login.
        """
        super().__init__(id)
        self.worker_id = worker_id
        self.username = username
        self.password = password