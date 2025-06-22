class BorrowMember:
    """Represents a member associated with a borrow record."""
    def __init__(self,  id_member:int, id_borrow:int):
        self.id_member = id_member
        self.id_borrow = id_borrow
