from .base import Base

class Library(Base):
    
    def __init__(self, id:int | None, name:str, fine_per_day: float, subscribe_amout:float, limit_borrow:int,borrow_price_with_sub:float, borrow_price_without_sub:float, borrow_delay:int,limit_reservation:int):
        """
        Initializes a new Library instance with a unique ID and a name.
        If an ID is provided, it will be used; otherwise, a new unique ID is generated.
        Args:
            id (int | None): Unique identifier for the library. If None, a new ID is generated.
            name (str): Name of the library.
            fine_per_day (float): Fine charged per day for overdue items.
            subscribe_amout (float): Subscription amount for the library.
            limit_borrow (int): Maximum number of items that can be borrowed at once.
            borrow_price_with_sub (float): Borrowing price for subscribers.
            borrow_price_without_sub (float): Borrowing price for non-subscribers.
            borrow_delay (int): Allowed borrowing delay in days.
        """

        super().__init__(id)
        self.name = name
        self.fine_per_day = fine_per_day
        self.subscribe_amout = subscribe_amout
        self.limit_borrow = limit_borrow
        self.borrow_price_with_sub = borrow_price_with_sub
        self.borrow_price_without_sub = borrow_price_without_sub
        self.borrow_delay = borrow_delay
        self.limit_reservation = limit_reservation
