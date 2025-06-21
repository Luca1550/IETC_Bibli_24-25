from repositories.models import Paiement, Member
from repositories import paiement_repo, paiement_member_repo
from .models import PaiementDTO
from datetime import date, datetime
from services import ExemplarService,LibraryService,MemberService,BorrowService
from enums import PaiementType

class PaiementService:
    def __init__(self):
        self.exemplar_service = ExemplarService()
        self.library_service=LibraryService()
        self.member_service=MemberService()
        self.borrow_service=BorrowService()

#crud + gestion des truc de library et relier au member
#pour avoir la date de retunr du livre, voir dans member truc
    #prendre date + retunr borrow date pour avooir le fine 



#calculer le retard
#Alin donne la date pour calculer le fine avec le borrow_retunr
def retunr(self,date):
    pass 