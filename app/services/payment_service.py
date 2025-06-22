from repositories.models import Payment,PaymentMember,ArchivePayment
from repositories import PaymentRepo, PaymentMemberRepo,ArchivePaymentRepo
from .models import PaymentDTO
from datetime import date, datetime
from services import ExemplarService,LibraryService,MemberService,BorrowService,BookService
from enums import PaymentType

class PaymentService:
    def __init__(self):
        """ Initialize the paymentService with necessary repositories and services. """
        self.exemplar_service = ExemplarService()
        self.library_service=LibraryService()
        self.member_service=MemberService()
        self.borrow_service=BorrowService()
        self.book_service=BookService()
        self.payment_repo=PaymentRepo()
        self.payment_member_repo=PaymentMemberRepo()
        self.archive_payment_repo = ArchivePaymentRepo()

    def add_payment(self,payment_type:int,payment_due:int,id_member:int):
        """ Add a new payment record and associate it with a member if provided."""
        try:
            new_payment = Payment(
                    id=None,  
                    payment_type=payment_type,
                    payment_due=payment_due,
                    payment_date=date.today().isoformat(), 
                )
            result = self.payment_repo.add_payment(new_payment)


            if result :
                if id_member:
                    new_payment_member= PaymentMember(
                        id_payment=new_payment.id,
                        id_member=id_member

                    )
                    

                    self.payment_member_repo.add_payment_member(new_payment_member)
            
            self.archive_payment(new_payment.id)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"🛑 Error [{e}]")
    def calculate_fine(self,date_from_member_return:date,id_borrow:int, return_date_planned:date):
        """ Calculate the fine for a late return based on the return date and library parameters."""
        try:
            libparams=self.library_service.get_library_parameters()
            return_fine_per_day=libparams[0].fine_per_day
            
            if datetime.fromisoformat(date_from_member_return).date() > datetime.fromisoformat(return_date_planned).date():
                return_delay=(datetime.fromisoformat(date_from_member_return).date()-datetime.fromisoformat(return_date_planned).date()).days
                payment_due:float = return_delay*return_fine_per_day
            return payment_due
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"🛑 Error [{e}]")
    def price_due_per_borrow(self,id_member:int,payment:Payment):
        """ Calculate the payment due for borrowing a book based on member subscription status."""
        try:
            libparams=self.library_service.get_library_parameters()
            borrow_price_with_sub_lib = libparams[0].borrow_price_with_sub
            borrow_price_without_sub_lib = libparams[0].borrow_price_without_sub
            if self.borrow_service.check_subscribe(id_member):
                payment.payment_due =borrow_price_with_sub_lib
                payment.payment_type= PaymentType(value=3)
            else:
                payment.payment_due =borrow_price_without_sub_lib
                payment.payment_type= PaymentType(value=4)
            
            return payment
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"🛑 Error [{e}]")
    
    

    def price_due_lost(self,is_it:bool,id_borrow:int,return_date_planned:date):
        """ Calculate the payment due for a lost book based on the borrow ID and member ID."""
        try:
            if is_it:
                paramborrow=self.borrow_service.get_by_id(id_borrow)
                paramexemp=self.exemplar_service.get_by_id(paramborrow.id_exemplar)
                parambook=self.book_service.get_by_isbn(paramexemp.isbn)
                payment_due=parambook.price
                
                self.borrow_service.delete_borrow(id_borrow)
                self.exemplar_service.delete_exemplar(paramborrow.id_exemplar)
            return payment_due
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"🛑 Error [{e}]")
    def get_all(self):
        """ Retrieve all payment records and return them as a list of paymentDTO objects."""
        try:
            payment = self.payment_repo.get_payment_parameters()
            result : list[PaymentDTO] = []

            for p in payment:
                pai_id = p.id
                pai_type=p.payment_type
                pai_due=p.payment_due
                pai_date=p.payment_date
                member=self.payment_member_repo.get_members_by_payment(pai_id)
                payment_dto = PaymentDTO(
                    id_payment=pai_id,
                    member=member,
                    payment_type=pai_type,
                    payment_due=pai_due,
                    payment_date=pai_date
                    
                )
                result.append(payment_dto)
            return result
        except Exception as e:
            raise Exception(f"🛑 Error getting payments: [{e}]")
    def get_by_id(self,id:int):
        """ Retrieve a payment record by its ID and return it as a paymentDTO object."""
        try:
            paymentDTO = self.get_all()
            for payment in paymentDTO :
                if payment.id_payment == id:
                    return payment
            else:
                raise Exception(f"payment with the given ID : {id} was not found.")
        except Exception as e:
            raise Exception(f"🛑 Error getting payment by ID: [{e}]")
        
    def archive_payment(self,id_payment:int):
        """ Archive a payment record by its ID."""
        try:
            payment = self.payment_repo.get_by_id(id_payment)
            payment_dto = self.get_by_id(id_payment)
            id_archive=None
            archive=ArchivePayment(
                    id=id_archive,
                    id_payment=payment.id,
                    member=payment_dto.member,
                    payment_type=payment.payment_type,
                    payment_due=payment.payment_due,
                    payment_date=payment.payment_date
                )
            self.archive_payment_repo.add_archive_payment(archive)
        except Exception as e:
            raise Exception(f"🛑 Error getting payment by ID: [{e}]")
    def gen_price(self,id_borrow:int,is_it:bool,id_member:int,return_date_planned:date):
        date_from_member_return=date.today().isoformat()
        payment=Payment(
            id=None,
            payment_type=None,
            payment_due=None,
            payment_date=None        

        )
        payment=self.price_due_per_borrow(id_member,payment)
        if is_it:
            payment.payment_due += float(self.price_due_lost(is_it,id_borrow,id_member))
            payment.payment_type = PaymentType(value=2)
        else:
            if datetime.fromisoformat(date_from_member_return).date() > datetime.fromisoformat(return_date_planned).date():
                payment.payment_due += float(self.calculate_fine(date_from_member_return,id_borrow,return_date_planned))
                payment.payment_type = PaymentType(value=1)
            self.borrow_service.delete_borrow(id_borrow)

        payment.payment_date=date.today().isoformat()
        
        self.add_payment(payment.payment_type,payment.payment_due,id_member)
        return payment.payment_due
    