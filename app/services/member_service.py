from repositories.models import Member, Person
from repositories import MemberRepo, PersonRepo, BorrowMemberRepo, BorrowRepo, ReservationMemberRepo
from services import PersonService, BookService, ExemplarService
from services.models import MemberDTO, BorrowDTO, BookDTO
from datetime import date

class MemberService:
    """
    Service for managing Member objects.
    """

    def __init__(self):
        self._member_repo = MemberRepo()
        self._person_repo = PersonRepo()
        self._person_service = PersonService()
        self._borrow_member_repo = BorrowMemberRepo()
        self._reservation_member_repo = ReservationMemberRepo()
        self._borrow_repo = BorrowRepo()
        self._book_service = BookService()
        self._exemplar_service = ExemplarService()


    def add_member(self, id : int, first_name : str, last_name : str, national_number: str, email : str, street : str, cp : str, city : str, membership_entrydate : date, subscribed : bool, archived : bool) -> MemberDTO:
        """
        Adds a Member object to the repository.
        :param member: Member object to be added.
        :return: True if the member was added successfully, False otherwise.
        """
        try:
            person = self._person_service.add_person(
                first_name,
                last_name,
                national_number,
                email,
                street,
                cp,
                city
            )
            if isinstance(person, Person):
                member = Member(
                    id=id,
                    id_person=person.id,
                    membership_entrydate=membership_entrydate,
                    subscribed=subscribed,
                    archived=archived
                )
                self._member_repo.add_member(member)
                return MemberDTO(
                    id_member=member.id,
                    person=person,
                    membership_entrydate=member.membership_entrydate,
                    subscribed=member.subscribed,
                    archived=member.archived
                )
            else:
                raise Exception("Failed to add person.")
        except Exception as e:
            raise Exception(f"🛑 Error adding member: {e}")

    def update_member(self, id: int, first_name: str, last_name: str, national_number: str, email: str, street: str, cp: str, city: str, membership_entrydate: date, subscribed: bool, archived: bool) -> bool:
       
        member = self._member_repo.get_member_by_id(id)
        if not member:
            raise Exception("Member not found for update.")
        success = self._person_service.update_person(
            member.id_person,
            first_name,
            last_name,
            national_number,
            email,
            street,
            cp,
            city
        )
        if success:
            # Mettre à jour les champs du membre existant
            member.membership_entrydate = membership_entrydate
            member.subscribed = subscribed
            member.archived = archived
            
            # Sauvegarder le membre mis à jour dans le repo
            self._member_repo.update_member(member)
            return True

        raise Exception("Person update failed.")

    def get_member_by_id(self, id: int) -> MemberDTO | None:
        """
        Retrieves a Member object by its ID.
        :param id: ID of the Member to retrieve.
        :return: Member object if found, None otherwise.
        """
        member = self._member_repo.get_member_by_id(id)
        if member:
            person = self._person_repo.get_by_id(member.id_person)
            if person:
                return MemberDTO(
                    id_member=member.id,
                    person=person,
                    membership_entrydate=member.membership_entrydate,
                    subscribed=member.subscribed,
                    archived=member.archived
                )
        return None

    def delete_member(self, id: int) -> bool:
        """
        Deletes a Member object from the repository.
        :param member: Member object to be deleted.
        :return: True if the member was deleted successfully, False otherwise.
        """
        try:
            member = self._member_repo.get_member_by_id(id)
            if self._borrow_member_repo.get_borrow_by_member(id) or self._reservation_member_repo.get_reservation_member(id):
                raise Exception("Cannot delete member with active borrows or reservations.")
            if member:
                self._member_repo.delete_member(member)
                self._person_service.delete_person(member.id_person)
                return True
            else:
                raise Exception(f"Member with the given ID : {id} was not found.")
        except Exception as e:
            raise Exception(f"🛑 Error [{e}]")
        
    def get_all_members(self) -> list[MemberDTO]:
        """
        Retrieves all Member objects from the repository.
        :return: A list of all Member objects.
        """
        members = self._member_repo.get_all_members()
        member_dtos = []
        for member in members:
            person = self._person_repo.get_by_id(member.id_person)
            if person:
                member_dtos.append(MemberDTO(
                    id_member=member.id,
                    person=person,
                    membership_entrydate=member.membership_entrydate,
                    subscribed=member.subscribed,
                    archived=member.archived
                ))
        return member_dtos
    
    def get_borrowed_books(self, member_id: int) -> list[BorrowDTO]:
        """
        Retrieves all borrowed books for a specific member.
        :param member_id: ID of the member.
        :return: A list of BorrowDTO objects representing borrowed books.
        """
        borrows = self._borrow_member_repo.get_borrow_by_member(member_id)
        borrow_dtos = []
        for borrow in borrows:
            borrow_check = self._borrow_repo.get_by_id(borrow.id_borrow)
            if not borrow_check:
                continue
            borrow_dto = BorrowDTO(
                id_borrow=borrow.id_borrow,
                id_exemplar=borrow_check.id_exemplar,
                member=self.get_member_by_id(member_id),
                borrow_date=borrow_check.borrow_date,
                return_date=borrow_check.return_date,
                
            )
            borrow_dtos.append(borrow_dto)
        return borrow_dtos
    
    def get_book_by_exemplar_id(self, exemplar_id: int) -> BookDTO | None:
        exemplar = self._exemplar_service.get_by_id(exemplar_id)
        book = self._book_service.get_by_isbn(exemplar.isbn) if exemplar else None
        # If the exemplar is found, retrieve the book by its ISBN
        if book:
            return BookDTO(
                isbn=book.isbn,
                title=book.title,
                authors=book.authors,
                date=book.date,
                price=book.price,
                editors=book.editors,
                collection=book.collection,
                themes=book.themes
            )
        return None