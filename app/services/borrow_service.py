from repositories.models import Borrow, Member,BorrowMember
from repositories import BorrowRepo, MemberRepo, BookRepo, ExemplarRepo,BorrowMemberRepo
from .models import BorrowDTO
from datetime import date, datetime,timedelta
from services import ExemplarService,LibraryService,MemberService,ReservationService
from enums import PaymentType

class BorrowService:
    def __init__(self):
        self._borrow_repo = BorrowRepo()
        self._exemplar_repo = ExemplarRepo()
        self._member_repo = MemberRepo()
        self._book_repo = BookRepo()
        self._borrow_member_repo = BorrowMemberRepo()
        self._reservation_service = ReservationService()
        self.exemplar_service = ExemplarService()
        self.library_service = LibraryService()
        self.member_service= MemberService()

    def check_borrow_limit(self,id_member:int):
        try:
            libparms=self.library_service.get_library_parameters()
            limit_borrow = libparms[0].limit_borrow
            if id_member:
                borrow_list_member=self._borrow_member_repo.get_borrow_by_member(id_member)
            if not len(borrow_list_member) < limit_borrow:
                raise Exception("Borrow limit reached for this member.")
            return True
        except Exception as e:
            raise Exception(e)
    
    def return_borrow_date(self,date_borrow:date):
        try:
            if date_borrow:
                libparms=self.library_service.get_library_parameters()
                return_date_lib = libparms[0].borrow_delay
                return_date=(datetime.fromisoformat(date_borrow).date() + timedelta(days=return_date_lib)).isoformat()
                return return_date
        except Exception as e:
            raise Exception(e)
            
    def check_subscribe(self,id_member:int):
        try:
            memberparms=self.member_service.get_member_by_id(id_member)
            return memberparms.subscribed
        except Exception as e:
            raise Exception(e)
        

    def add_borrow(self, isbn : str | None, id_member : int, id_exemplar : int | None = None, id_reservation : int | None = None):
        try:
            actual_borrow_date = date.today().isoformat()
            if not id_exemplar:
                exemplar=self.exemplar_service.get_disponibility(isbn)
            else:
                exemplar=self.exemplar_service.get_by_id(id_exemplar)
            return_date=self.return_borrow_date(actual_borrow_date)
            if self.check_borrow_limit(id_member):
                new_borrow = Borrow(
                    id=None,
                    id_exemplar=exemplar.id,
                    borrow_date=actual_borrow_date,
                    return_date = return_date,
                    )

                if self._borrow_repo.add_borrow(new_borrow) :
                    if id_member:
                        new_borrow_member= BorrowMember(
                            id_borrow=new_borrow.id,
                            id_member=id_member
                        )
                        self._borrow_member_repo.add_borrow_member(new_borrow_member) 
            if id_reservation is not None:
                self._reservation_service.delete_reservation(id_reservation)
            self.exemplar_service.update_status(exemplar.id,2)
            return True
        except Exception as e:
            raise Exception(f"🛑 Error when add borrow [{e}]")
        
    
    def get_all(self):
        try:
            borrows = self._borrow_repo.get_borrows()
            result : list[BorrowDTO] = []

            for bor in borrows:
                member = self._borrow_member_repo.get_borrow_member_by_id(bor.id)
                
                borrow_dto = BorrowDTO(
                    id_borrow = bor.id,
                    id_exemplar = bor.id_exemplar,
                    member = member,
                    borrow_date = bor.borrow_date,
                    return_date = bor.return_date,
                )
                result.append(borrow_dto)
            return result
        except Exception as e:
            raise Exception(f"🛑 Error getting borrow: [{e}]")
        
    def get_by_id(self,id:int):
        try:
            BorrowDTO = self.get_all()
            for borrow in BorrowDTO : 
                if borrow.id_borrow == id:
                    return borrow
            else:
                raise Exception(f"Borrow with the given ID : {id} was not found.")
        except Exception as e:
            raise Exception(f"🛑 Error [{e}]")

    def delete_borrow(self,id:int):
        """
        Deletes a borrow by its ID."""
        try:
            borrow = self._borrow_repo.get_by_id(id)
            borrow_dto = self.get_by_id(id)

            if isinstance(borrow, Borrow):
                self._borrow_repo.delete_borrow(borrow)
            self.exemplar_service.update_status(borrow.id_exemplar,1)
            if borrow_dto and isinstance(borrow_dto.member, Member):
                self._borrow_member_repo.delete_borrow_member(
                    id_member=borrow_dto.member.id,
                    id_borrow=id
                )
            return True
        except Exception as e:
            raise Exception(f"🛑 Error deleting borrow: [{e}]")
        