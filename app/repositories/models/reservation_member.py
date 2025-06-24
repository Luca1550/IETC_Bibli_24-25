class ReservationMember:
    """
    Model representing the association between a reservation and a member.
    """
    def __init__(self, id_reservation: int, id_member: int):
        self.id_reservation = id_reservation
        self.id_member = id_member

        
