# tout importer de reservation et member dans les mode, repo et aussi le dto mais aussi l'exemplar car on va prendre son id 
from repositories.models import Reservation,Member,Exemplar,Library,ReservationMember
from repositories import ReservationRepo,ExemplarRepo,MemberRepo,ReservationMemberRepo,BookRepo,LibraryRepo
from .models import ReservationDTO
from datetime import date, datetime


#NOTE POUR JULEN/ BUG RECUP DE L ID MEMBER ET RECUP AVEC LE NOM 
class ReservationService:

    def __init__(self):
        self._reservation_repo = ReservationRepo()
        self._exemplar_repo = ExemplarRepo()
        self._member_repo = MemberRepo()
        self._reservation_member_repo= ReservationMemberRepo()
        self._book_repo = BookRepo()
        


#faut que je rajoute le temps de reservation dans library du coup je dois aussi aller rechercher l'id de library pour avoir l'info et calculer ta grosse mere  
#ajoute
#on a un probleme ok ca va add tout ca mais alors je dois aussi add dans mon dto et comment on va relier le nom de la personne avec son id
#ahhh bah par le dto en fait donc quand je vais faire un add je vais donner son nom, je vais le check dans le dto par son id qui va etre renvoyé ici 


#je dois encore rrajouter une fonction qui permet en donnant le isbn d'avoir l'id de l'exemplar je vais utiliser le get all by isbn 
    def get_exemplar_by_name(self, title: str) -> int | None:
        try:
            books = self._book_repo.get_all()
            for b in books:
                # Accès en mode dictionnaire si les objets sont des dicts
                book_title = b.title 
                isbn = b.isbn 
                print("Checking book title:", book_title, "ISBN:", isbn)
                if book_title.lower() == title.lower():
                    exemplars = self._exemplar_repo.get_all(isbn)
                    print("book found for book title:", title, "ISBN:", isbn)
                    if exemplars:
                        print("Exemplars found for book title:", title, "ISBN:", isbn)
                        return exemplars[0].id
            raise Exception(f"Book with title '{title}' not found.")
        except Exception as e:
            print(f"🛑 Error getting exemplar by book title: [{e}]")
            return None

        
    def add_reservation(self,id_exemplar:int,id_member:int,reservation_date:date|None = None) ->Reservation:

        try:
            if reservation_date is None:
                actual_reservation_date = date.today().isoformat()
            else:
                if isinstance(reservation_date, str):
                    actual_reservation_date = datetime.fromisoformat(reservation_date).date().isoformat()
                else:
                    actual_reservation_date = reservation_date.isoformat()
            new_reservation = Reservation(
                id=None,
                id_exemplar=id_exemplar,
                reservation_date=actual_reservation_date
                )
            #ici je dois changer le statuut de exemplar 

            result=self._reservation_repo.add_reservation(new_reservation)
            reservation_member_result = None
            paramres=self.get_parameter_reservation()
            if result :
                #je check si l'id existe bien dans result 

                if id_member:
                    id_new_res = paramres[-1].id_exemplar
                    new_reservation_member= ReservationMember(
                        id_reservation=id_new_res,
                        id_member=id_member
                    )
                    reservation_member_result = self._reservation_member_repo.add_reservation_member(new_reservation_member) 
            return result,reservation_member_result
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"🛑 Error [{e}]"
    def get_all(self):
        try:
            reservations = self._reservation_repo.get_reservation_parameters()
            result : list[ReservationDTO] = []

            for res in reservations:
                res_id = res.id
                res_exemplar = res.id_exemplar
                res_date = res.reservation_date
                member = self._reservation_member_repo.get_reservation_member_byId(res_id)

                reservation_dto = ReservationDTO(
                    id_reservation=res_id,
                    id_exemplar=res_exemplar,
                    member=member,
                    reservation_date=res_date
                )
                result.append(reservation_dto)
            
            return result
        except Exception as e:
            print(f"🛑 Error getting reservations: [{e}]")
            return []
        
    def get_by_id(self,id:int):
        try:
            reservationsDTO = self.get_all()
            for reservation in reservationsDTO : 
                if reservation.id == id:
                    return reservation
            else:
                raise Exception(f"Reservation with the given ID : {id} was not found.")
        except Exception as e:
            print(f"🛑 Error getting reservation by ID: [{e}]")
            return None

    def delete_reservation(self,id_reservation:int):
        try:
            """reservation: Reservation = self._reservation_repo.get_by_id(id_reservation)
            reservation_DTO: ReservationDTO = self.get_by_id(id_reservation)
            for res in reservation:
                if res.id == id_reservation:
                    self._reservation_repo.delete_reservation(res.id, res.id_exemplar, res.reservation_date)
            for res in reservation_DTO:
                if res.id_reservation == id_reservation:
                    self._reservation_member_repo.delete_reservation_member(res.id_reservation, res.id_member)"""
            reservation = self._reservation_repo.get_by_id(id_reservation)
            reservation_dto = self.get_by_id(id_reservation)

            if isinstance(reservation, Reservation):
                self._reservation_repo.delete_reservation(reservation)
            
            if reservation_dto and isinstance(reservation_dto.member, Member):
                self._reservation_member_repo.delete_reservation_member(
                    id_member=reservation_dto.member.id,
                    id_reservation=id_reservation
                )
            return True
        except Exception as e:
            print(f"🛑 Error deleting reservation: [{e}]")
            return False
    def update_reservation(self,id:int,id_exemplar:int,id_member:int,reservation_date:date|None = None):
        try:
            reservation: Reservation = self._reservation_repo.get_by_id(id)
            reservation_DTO: ReservationDTO = self.get_by_id(id)

            if not isinstance(reservation, Reservation):
                raise Exception(f"Reservation with ID: {id} was not found.")
            if not isinstance(reservation_DTO, ReservationDTO):
                raise Exception(f"DTO for reservation ID: {id} was not found.")
            if id_exemplar is not None:
                reservation.id_exemplar = id_exemplar
            if reservation_date is not None:
                reservation.reservation_date = reservation_date
            print(reservation)
            self._reservation_repo.update_reservation(reservation)
            #ici je dois changer le statuut de exemplar 
            if id_member is not None:
                print('' * 50)
                print(f"reservation_DTO.member.id: {reservation_DTO.member.id}, id: {id}")
                self._reservation_member_repo.delete_reservation_member(id_member=reservation_DTO.member.id, id_reservation=id)
                new_res_member = ReservationMember(id_reservation=id, id_member=id_member)
                self._reservation_member_repo.add_reservation_member(new_res_member)
            return reservation
        except Exception as e:
            print(f"🛑 Error updating reservation: [{e}]")
            return None
            
    def get_parameter_reservation(self):
        return self._reservation_repo.get_reservation_parameters()
    
    def check_value(self,id_exemplar:int,reservation_date:date|None)-> Exception | bool:
        try:
            if not id_exemplar >= 0 or  not isinstance(id_exemplar, (int)):
                raise Exception("Invalid id exemplar.")
            if not isinstance(reservation_date, (date)):
                raise Exception("Invalid reservationdate: it must be a date like YYYY-MM-DD")
        except Exception as e:
            return f"🛑 Error [{e}]"
    #pour le add je dois encore changer le statut et check si ils sont deja reservé ou pas
    #ca ca va etre utile pour la liste
    def get_isbn_by_id_exemplar(self, id_exemplar: int):
        try:
            exemplar = self._exemplar_repo.get_by_id(id_exemplar)
            if isinstance(exemplar, Exemplar):
                book = self._book_repo.get_by_isbn(exemplar.isbn)
                if book:
                    return book.isbn
            raise Exception(f"Exemplar with ID {id_exemplar} not found.")
        except Exception as e:
            print(f"🛑 Error getting ISBN by exemplar ID: [{e}]")
            return ""
