class BorrowMember:
    """Represents a member associated with a borrow record."""
    def __init__(self, id:int, id_member:int, id_borrow:int):
        super().__init__(id)
        self.id_member = id_member
        self.id_borrow = id_borrow
