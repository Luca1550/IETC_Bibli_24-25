# tout importer de reservation et member dans les mode, repo et aussi le dto mais aussi l'exemplar car on va prendre son id 
from repositories.models import Reservation,Member,Exemplar,Library
from repositories import ReservationRepo,ExemplarRepo,MemberRepo,ReservationMemberRepo,BookRepo,LibraryRepo
from .models import ReservationDTO
from datetime import datetime

class ReservationService:

    def __init__(self):
        self._reservation_repo = ReservationRepo()
        self._exemplar_repo = ExemplarRepo()
        self._member_repo = MemberRepo()
        self._reservation_member_repo= ReservationMemberRepo()
        self._book_repo = BookRepo()


#faut que je rajoute le temps de reservation dans library du coup je dois aussi aller rechercher l'id de library pour avoir l'info et calculer ta grosse mere  

    def add_reservation(self,id_exemplar:int,id_member:int,reservation_date:datetime):
        pass
