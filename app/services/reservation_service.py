from repositories.models import Reservation,Member,Exemplar,Library,ReservationMember,ArchiveReservation
from repositories import ReservationRepo,ExemplarRepo,MemberRepo,ReservationMemberRepo,BookRepo,ArchiveReservationRepo
from .models import ReservationDTO
from datetime import date, datetime
from services import ExemplarService,LibraryService


class ReservationService:
    """
    Service for managing reservations in a library system."""

    def __init__(self):
        """
        Initializes the ReservationService with repositories for reservations, exemplars, members, and reservation members."""
        self._reservation_repo = ReservationRepo()
        self._exemplar_repo = ExemplarRepo()
        self._member_repo = MemberRepo()
        self._reservation_member_repo= ReservationMemberRepo()
        self._book_repo = BookRepo()
        self.archive_reservation_repo = ArchiveReservationRepo()
        self.exemplar_service = ExemplarService()
        self.library_service = LibraryService()


    def get_exemplar_by_name(self, title: str):
        """
        Retrieves the exemplar ID by book title."""
        try:
            books = self._book_repo.get_all()
            for b in books:
                book_title = b.title 
                isbn = b.isbn 
                if book_title.lower() == title.lower():
                    exemplars = self._exemplar_repo.get_all(isbn)
                    if exemplars:
                        return exemplars[0].id
            raise Exception(f"Book with title '{title}' not found.")
        except Exception as e:
            raise Exception(f"🛑 Error getting exemplar by book title: [{e}]")
            

        
    def add_reservation(self,isbn:str,id_member:int,reservation_date:date|None = None) :
        """
        Adds a reservation for a book by its ISBN and member ID.
        If reservation_date is None, it defaults to today's date.
        If the exemplar is not available, it raises an exception.
        """
        try:
            if reservation_date is None:
                actual_reservation_date = date.today().isoformat()
            else:
                if isinstance(reservation_date, str):
                    actual_reservation_date = datetime.fromisoformat(reservation_date).date().isoformat()
                else:
                    actual_reservation_date = reservation_date.isoformat()
            exemplar=self.exemplar_service.get_disponibility(isbn)
            if not exemplar:
                id_exemplars=self.exemplar_service.get_all_by_isbn(isbn)
                exemplar= next((exemplar for exemplar in id_exemplars if exemplar.status.value == 2))
                if not exemplar:
                    raise Exception("🛑 Error no exemplar") 
            new_reservation = Reservation(
                id=None,
                id_exemplar=exemplar.id,
                reservation_date=actual_reservation_date
                )
            if exemplar.status.value == 1:
                self.exemplar_service.update_status(exemplar.id,3)

            result=self._reservation_repo.add_reservation(new_reservation)
            reservation_member_result = None
            if result :

                if id_member:
                    id_new_res = new_reservation.id
                    new_reservation_member= ReservationMember(
                        id_reservation=id_new_res,
                        id_member=id_member
                    )
                    reservation_member_result = self._reservation_member_repo.add_reservation_member(new_reservation_member) 
            return result,reservation_member_result
        
        except Exception as e:
            return f"🛑 Error [{e}]"
    def get_all(self):
        """
        Retrieves all reservations and returns them as a list of ReservationDTO objects."""
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
            raise Exception(f"🛑 Error getting reservations: [{e}]")
            
        
    def get_by_id(self,id:int):
        """
        Retrieves a reservation by its ID and returns it as a ReservationDTO object."""
        try:
            reservationsDTO = self.get_all()
            for reservation in reservationsDTO : 
                if reservation.id_reservation == id:
                    return reservation
            else:
                raise Exception(f"Reservation with the given ID : {id} was not found.")
        except Exception as e:
            raise Exception(f"🛑 Error getting reservation by ID: [{e}]")
            

    def delete_reservation(self,id_reservation:int):
        """
        Deletes a reservation by its ID."""
        try:
            
            reservation = self._reservation_repo.get_by_id(id_reservation)
            reservation_dto = self.get_by_id(id_reservation)
            id_archive=None
            

            archive=ArchiveReservation(
                id=id_archive,
                id_reservation=reservation.id,
                id_exemplar=reservation.id_exemplar,
                reservation_date=reservation.reservation_date,
                member=reservation_dto.member
            )
            if isinstance(reservation, Reservation):
                self._reservation_repo.delete_reservation(reservation)
            
            if reservation_dto and isinstance(reservation_dto.member, Member):
                self._reservation_member_repo.delete_reservation_member(
                    id_member=reservation_dto.member.id,
                    id_reservation=id_reservation
                )
            self.exemplar_service.update_status(reservation.id_exemplar, 1)
            self.archive_reservation_repo.add_archive_reservation(archive)
            return True
        except Exception as e:
            raise Exception(f"🛑 Error deleting reservation: [{e}]")
    def update_reservation(self,id:int,id_member:int,reservation_date:date|None = None):
        """
        Updates a reservation by its ID.
        If reservation_date is provided, it updates the reservation date.
        If id_member is provided, it updates the reservation member.
        Returns the updated reservation object."""
        try:
            reservation: Reservation = self._reservation_repo.get_by_id(id)
            reservation_DTO: ReservationDTO = self.get_by_id(id)

            if not isinstance(reservation, Reservation):
                raise Exception(f"Reservation with ID: {id} was not found.")
            if not isinstance(reservation_DTO, ReservationDTO):
                raise Exception(f"DTO for reservation ID: {id} was not found.")
            if reservation_date is not None:
                reservation.reservation_date = reservation_date
            self._reservation_repo.update_reservation(reservation)
            if id_member is not None:
                
                self._reservation_member_repo.delete_reservation_member(id_member=reservation_DTO.member.id, id_reservation=id)
                new_res_member = ReservationMember(id_reservation=id, id_member=id_member)
                self._reservation_member_repo.add_reservation_member(new_res_member)
            return reservation
        except Exception as e:
            raise Exception(f"🛑 Error updating reservation: [{e}]")
            
    def get_parameter_reservation(self):
        """
        Retrieves reservation parameters from the repository.
        Returns a list of reservation parameters."""
        return self._reservation_repo.get_reservation_parameters()
    
    def check_value(self,id_exemplar:int,reservation_date:date|None)-> Exception | bool:
        """
        Checks if the provided id_exemplar and reservation_date are valid.
        If valid, returns True; otherwise, raises an exception with an error message."""
        try:
            if not id_exemplar >= 0 or  not isinstance(id_exemplar, (int)):
                raise Exception("Invalid id exemplar.")
            if not isinstance(reservation_date, (date)):
                raise Exception("Invalid reservationdate: it must be a date like YYYY-MM-DD")
        except Exception as e:
            return f"🛑 Error [{e}]"

    def get_isbn_by_id_exemplar(self, id_exemplar: int):
        """
        Retrieves the ISBN of a book by its exemplar ID.
        If the exemplar is found, returns its ISBN; otherwise, raises an exception."""
        try:
            exemplar = self._exemplar_repo.get_by_id(id_exemplar)
            if isinstance(exemplar, Exemplar):
                book = self._book_repo.get_by_isbn(exemplar.isbn)
                if book:
                    return book.isbn
            raise Exception(f"Exemplar with ID {id_exemplar} not found.")
        except Exception as e:
            raise Exception(f"🛑 Error getting ISBN by exemplar ID: [{e}]")