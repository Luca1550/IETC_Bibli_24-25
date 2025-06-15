# tout importer de reservation et member dans les mode, repo et aussi le dto mais aussi l'exemplar car on va prendre son id 
from repositories.models import Reservation,Member,Exemplar,Library,ReservationMember
from repositories import ReservationRepo,ExemplarRepo,MemberRepo,ReservationMemberRepo,BookRepo,LibraryRepo
from .models import ReservationDTO
from datetime import date

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
    def add_reservation(self,id_exemplar:int,id_member:int,reservation_date:date|None) ->Reservation:
        self.paramres_wt_DTO = self.get_parameter_reservation_wtDTO()


        try:
            if reservation_date is None:
                actual_reservation_date = date.today()
            else:
                actual_reservation_date = reservation_date
            validation_result = self.check_value(id_exemplar, actual_reservation_date)
            if isinstance(validation_result, str):
                return validation_result 
                
            new_reservation = Reservation(
                id=None,
                id_exemplar=id_exemplar,
                reservation_date=actual_reservation_date
                )
                
            result=self._reservation_repo.add_reservation(new_reservation)
            if result and id_member: 
                new_reservation_member= ReservationMember(
                    #faut check le id c'est pas bon
                    id_reservation=result.id_reservation,
                    id_member=id_member
                )
                reservation_member_result = self._reservation_member_repo.add_reservation_member(new_reservation_member) 
            return result
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"🛑 Error [{e}]"
    def get_all(self):
        try:
            reservations = self._reservation_repo.get_reservation_parameters()
            result = []

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
    def delete_reservation(self):
        pass

    def update_reservation(self):
        pass
    def get_parameter_reservation_wtDTO(self):
        return self._reservation_repo.get_reservation_parameters()
    
    def check_value(self,id_exemplar:int,reservation_date:date|None)-> Exception | bool:
        try:
            if not id_exemplar >= 0 or  not isinstance(id_exemplar, (int)):
                raise Exception("Invalid id exemplar.")
            #if not id_member >= 0 or not isinstance(id_member, (int)):
            #    raise Exception("Invalid idmember.")
            if not isinstance(reservation_date, (date)):
                raise Exception("Invalid reservationdate: it must be a date like YYYY-MM-DD")
        except Exception as e:
            return f"🛑 Error [{e}]"
