from repositories.models import Base
from datetime import date

class Reservation(Base):
    """
    Represents a reservation for an exemplar in the library system.
    """
    def __init__(self, id : int | None, id_exemplar : int, reservation_date : date):
        """
        Initializes a Reservation instance with the provided parameters.
        :param id: Unique identifier for the reservation.
        :param id_exemplar: Unique identifier for the exemplar being reserved.
        :param reservation_date: Date of the reservation.
        """
    
        super().__init__(id)
        self.id_exemplar=id_exemplar
        self.reservation_date=reservation_date