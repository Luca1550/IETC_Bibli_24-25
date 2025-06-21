from repositories.models import Borrow, Member,Library,Exemplar,BorrowMember
from repositories import BorrowRepo, MemberRepo, BookRepo, ExemplarRepo,BorrowMemberRepo
from .models import BorrowDTO
from datetime import date, datetime,timedelta
from services import ExemplarService,LibraryService,MemberService


class BorrowService:
    def __init__(self):
        self._borrow_repo = BorrowRepo()
        self._exemplar_repo = ExemplarRepo()
        self._member_repo = MemberRepo()
        self._borrow_member_repo= BorrowMemberRepo()
        self._book_repo = BookRepo()
        self.exemplar_service = ExemplarService()
        self.library_service = LibraryService()
        self.member_service= MemberService()
#supp limit borrow dans les param et le recup direct 
    def check_borrow_limit(self,id_member:int):
        try:
            libparms=self.library_service.get_library_parameters()
            limit_borrow = libparms[0].limit_borrow
            if id_member:
                borrow_list_member=self._borrow_member_repo.get_borrow_members()
                for bor in borrow_list_member:
                    count = sum(1 for bor in borrow_list_member if bor.id_member == id_member)
                    return count 
            if count < limit_borrow:
                return True
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"🛑 Error [{e}]"
    
    def return_borrow_date(self,date_borrow:date):
        try:
            if date_borrow:
                libparms=self.library_service.get_library_parameters()
                return_date_lib = libparms[0].borrow_delay
                return_date=(datetime.fromisoformat(date_borrow).date() + timedelta(days=return_date_lib)).isoformat()
                return return_date
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"🛑 Error [{e}]"
    def calculate_fine(self, return_date:date, borrow_date:date):
        """Calculates the fine for overdue borrows.
        arguments:
        - return_date: The date the item was returned.
        - borrow_date: The date the item was borrowed.
        - fine_per_day: The fine amount per day of delay.
        returns:
        - The total fine amount if the item is overdue, otherwise returns 0."""
        libparms=self.library_service.get_library_parameters()
        return_fine_per_day = libparms[0].fine_per_day
        if return_date and borrow_date:
            days_overdue = (return_date - borrow_date).days
            if days_overdue > 0:
                fine =days_overdue * return_fine_per_day
                return fine
    
    def price_borrow_member(self,id_member:int):
        try:
            libparms=self.library_service.get_library_parameters()
            borrow_price_with_sub_lib = libparms[0].borrow_price_with_sub
            borrow_price_without_sub_lib = libparms[0].borrow_price_without_sub
            memberparms=self.member_service.get_member_by_id(id_member)
            subscribed=memberparms.subscribed
            if subscribed == True:
                LaPLata = borrow_price_with_sub_lib
            else:
                LaPLata = borrow_price_without_sub_lib
            return LaPLata
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"🛑 Error [{e}]"
    def add_borrow(self, isbn:str,id_member:int, borrow_date:date|None,paiement_type:int,paiement_status:int):
        
        try:
            if borrow_date is None:
                actual_borrow_date = date.today().isoformat()
            else:
                if isinstance(borrow_date, str):
                    actual_borrow_date = datetime.fromisoformat(borrow_date).date().isoformat()
                else:
                    actual_borrow_date = borrow_date.isoformat()
            exemplar=self.exemplar_service.get_disponibility(isbn)
            if not exemplar:
                id_exemplars=self.exemplar_service.get_all_by_isbn(isbn)
                # attention si reserver quid au pire amélioration future
                exemplar= next((exemplar for exemplar in id_exemplars if exemplar.status.value ==1))
            return_date=self.return_borrow_date(actual_borrow_date)
            paiement_due=self.price_borrow_member(id_member)
            if self.check_borrow_limit(id_member):
                new_borrow = Borrow(
                    id=None,
                    id_exemplar=exemplar.id,
                    borrow_date=actual_borrow_date,
                    return_date = return_date,
                    paiement_due = paiement_due,
                    paiement_type = paiement_type,
                    #paiement_status faudra voir dans l'ui cette folle
                    paiement_status = paiement_status
                    )
                print("id_exemplar  ",exemplar.id)
                self.exemplar_service.update_status(exemplar.id,2)

                result=self._borrow_repo.add_borrow(new_borrow)
                borow_member_result = None
                if result :

                    if id_member:
                        id_new_borrow = new_borrow.id
                        new_borrow_member= new_borrow(
                            id_reservation=id_new_borrow,
                            id_member=id_member
                        )
                        borow_member_result = self._borrow_member_repo.add_borrow_member(new_borrow_member) 
            return result,borow_member_result
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"🛑 Error [{e}]"
    def get_all(self):
        try:
            borrows = self._borrow_repo.get_borrows()
            result : list[BorrowDTO] = []

            for bor in borrows:
                bor_id = bor.id
                bor_exemplar = bor.id_exemplar
                bor_date = bor.borrow_date
                bor_ret_date=bor.borrow_date
                bor_paiement_due= bor.paiement_due
                bor_paiement_due = bor.paiement_due
                bor_paiement_type = bor.paiement_type
                borpaiement_status = bor.paiement_status
                member = self._borrow_member_repo.get_borrow_member_by_id(bor_id)
                
                borrow_dto = BorrowDTO(
                    id_borrow = bor_id,
                    id_exemplar = bor_exemplar,
                    member = member,
                    borrow_date = bor_date,
                    return_date = bor_ret_date,
                    paiement_due = bor_paiement_due,
                    paiement_type = bor_paiement_type,
                    paiement_status = borpaiement_status
        
                )
                result.append(borrow_dto)
            
            return result
        except Exception as e:
            print(f"🛑 Error getting borrow: [{e}]")
            return []
        
    def get_by_id(self,id:int):
        try:
            BorrowDTO = self.get_all()
            for borrow in BorrowDTO : 
                if borrow.id_borrow == id:
                    return borrow
            else:
                raise Exception(f"Borrow with the given ID : {id} was not found.")
        except Exception as e:
            print(f"🛑 Error getting borrow by ID: [{e}]")
            return None
        
    # def update_borrow(self, id: int, id_member: int, borrow_date: date | None, paiement_type: int, paiement_status: int):
    #     try:
    #         borrow: Borrow = self._borrow_repo.get_by_id(id)
    #         borrow_dto: BorrowDTO = self.get_by_id(id)

    #         if not borrow:
    #             raise Exception(f"Borrow with ID: {id} was not found.")
    #         if not borrow_dto:
    #             raise Exception(f"DTO for borrow ID: {id} was not found.")

    #         if borrow_date is not None:
    #             if isinstance(borrow_date, str):
    #                 borrow.borrow_date = datetime.fromisoformat(borrow_date).date()
    #             elif isinstance(borrow_date, date):
    #                 borrow.borrow_date = borrow_date

    #         if not borrow.return_date:
    #             borrow.return_date = self.return_borrow_date(borrow.borrow_date)

    #         if paiement_type is not None:
    #             borrow.paiement_type = paiement_type
    #         if paiement_status is not None:
    #             borrow.paiement_status = paiement_status

    #         updated = self._borrow_repo.update_borrow(borrow)

    #         if id_member is not None:
    #             old_member = borrow_dto.member
    #             if old_member:
    #                 self._borrow_member_repo.delete_borrow_member(old_member.id_member, id)
    #             new_link = BorrowMember(id_borrow=id, id_member=id_member)
    #             self._borrow_member_repo.add_borrow_member(new_link)

    #         return updated

    #     except Exception as e:
    #         print(f"🛑 Error updating borrow: [{e}]")
    #         import traceback
    #         traceback.print_exc()
    #         return None

    def delete_borrow(self,id:int):
        """
        Deletes a borrow by its ID."""
        try:
            
            borrow = self._borrow_repo.get_by_id(id)
            borrow_dto = self.get_by_id(id)

            if isinstance(borrow, Borrow):
                self._borrow_repo.delete_borrow(borrow)
            
            if borrow_dto and isinstance(borrow_dto.member, Member):
                self._borrow_member_repo.delete_borrow_member(
                    id_member=borrow_dto.member.id,
                    id_borrow=id
                )
            return True
        except Exception as e:
            raise Exception(f"🛑 Error deleting borrow: [{e}]")
        
