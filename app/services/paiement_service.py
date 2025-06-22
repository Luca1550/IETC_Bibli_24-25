from repositories.models import Paiement, Member,PaiementMember,ArchivePaiement
from repositories import PaiementRepo, PaiementMemberRepo,ArchivePaiementRepo
from .models import PaiementDTO
from datetime import date, datetime
from services import ExemplarService,LibraryService,MemberService,BorrowService,BookService
from enums import PaiementType

class PaiementService:
    def __init__(self):
        self.exemplar_service = ExemplarService()
        self.library_service=LibraryService()
        self.member_service=MemberService()
        self.borrow_service=BorrowService()
        self.book_service=BookService()
        self.paiement_repo=PaiementRepo()
        self.paiement_member_repo=PaiementMemberRepo()
        self.archive_paiement_repo = ArchivePaiementRepo()  
#crud + gestion des truc de library et relier au member
#pour avoir la date de retunr du livre, voir dans member truc
    #prendre date + retunr borrow date pour avooir le fine 


    #     class PaiementType(Enum):
    # FINE=1
    # LOST_BOOK=2
    # BORROW_WITH_SUB=3
    # BORROW_WITHOUT_SUB=4


    def add_paiement(self,paiement_type:int,paiement_due:int,id_member:int):
        try:
            new_paiement = Paiement(
                    id=None,  
                    paiement_type=paiement_type,
                    paiement_due=paiement_due,
                    paiement_date=date.today().isoformat(), 
                )
            result = self.paiement_repo.add_paiement(new_paiement)


            paiement_member_result = None
            if result :
                if id_member:
                    new_paiement_member= PaiementMember(
                        id_paiement=new_paiement.id,
                        id_member=id_member

                    )
                    

                    paiement_member_result=self.paiement_member_repo.add_paiement_member(new_paiement_member)
            
            self.archive_paiement(new_paiement.id)
            return result,paiement_member_result
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"🛑 Error [{e}]")
    def calculate_fine(self,date_from_member_return:date,id_borrow:int,id_member:int):
        
        try:
            paiement_type = PaiementType(value=1)
            libparams=self.library_service.get_library_parameters()
            return_fine_per_day=libparams[0].fine_per_day
            borrowparams=self.borrow_service.get_by_id(id_borrow)
            return_date_planned=borrowparams.return_date
            
            if datetime.fromisoformat(date_from_member_return).date() > datetime.fromisoformat(return_date_planned).date():
                return_delay=(datetime.fromisoformat(date_from_member_return).date()-datetime.fromisoformat(return_date_planned).date()).days
                print('jouR',return_delay)
                paiement_due:float = return_delay*return_fine_per_day
                self.add_paiement(paiement_type,paiement_due,id_member)
            return paiement_due
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"🛑 Error [{e}]")
    def price_due_per_borrow(self,id_member:int):
        try:
            libparams=self.library_service.get_library_parameters()
            borrow_price_with_sub_lib = libparams[0].borrow_price_with_sub
            borrow_price_without_sub_lib = libparams[0].borrow_price_without_sub
            if self.borrow_service.check_subscribe(id_member):
                paiement_due = borrow_price_with_sub_lib
                paiement_type = PaiementType(value=3)
                self.add_paiement(paiement_type,paiement_due,id_member)
            else:
                paiement_due = borrow_price_without_sub_lib
                paiement_type = PaiementType(value=4)
                self.add_paiement(paiement_type,paiement_due,id_member)
            return paiement_due
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"🛑 Error [{e}]")
    
    

    def price_due_lost(self,is_it:bool,id_borrow:int,id_member:int):
        try:
            if is_it:
                paramborrow=self.borrow_service.get_by_id(id_borrow)
                paramexemp=self.exemplar_service.get_by_id(paramborrow.id_exemplar)
                parambook=self.book_service.get_by_isbn(paramexemp.isbn)
                paiement_due=parambook.price
                self.exemplar_service.delete_exemplar(paramborrow.id_exemplar)
                print("exemplar del")
                paiement_type = PaiementType(value=2)
                self.add_paiement(paiement_type,paiement_due,id_member)
            return paiement_due
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"🛑 Error [{e}]")
    def get_all(self):
        
        try:
            paiement = self.paiement_repo.get_paiement_parameters()
            result : list[PaiementDTO] = []

            for p in paiement:
                pai_id = p.id
                pai_type=p.paiement_type
                pai_due=p.paiement_due
                pai_date=p.paiement_date
                member=self.paiement_member_repo.get_members_by_paiement(pai_id)
                paiement_dto = PaiementDTO(
                    id_paiement=pai_id,
                    member=member,
                    paiement_type=pai_type,
                    paiement_due=pai_due,
                    paiement_date=pai_date
                    
                )
                result.append(paiement_dto)
            return result
        except Exception as e:
            raise Exception(f"🛑 Error getting paiements: [{e}]")
    def get_by_id(self,id:int):
        
        try:
            PaiementDTO = self.get_all()
            for paiement in PaiementDTO :
                if paiement.id_paiement == id:
                    return paiement
            else:
                raise Exception(f"Paiement with the given ID : {id} was not found.")
        except Exception as e:
            raise Exception(f"🛑 Error getting paiement by ID: [{e}]")
        
    def archive_paiement(self,id_paiement:int):
        try:
            paiement = self.paiement_repo.get_by_id(id_paiement)
            paiement_dto = self.get_by_id(id_paiement)
            id_archive=None
            archive=ArchivePaiement(
                    id=id_archive,
                    id_paiement=paiement.id,
                    member=paiement_dto.member,
                    paiement_type=paiement.paiement_type,
                    paiement_due=paiement.paiement_due,
                    paiement_date=paiement.paiement_date
                )
            self.archive_paiement_repo.add_archive_paiement(archive)
        except Exception as e:
            raise Exception(f"🛑 Error getting paiement by ID: [{e}]")
 