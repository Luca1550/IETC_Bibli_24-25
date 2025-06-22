import customtkinter as ctk
from tools import Color
from services.models import ReservationDTO
from services import ExemplarService, BookService, PersonService, ReservationService
from ui.components import PopUpMessage

class ReservationFrame(ctk.CTkFrame):
    """
    A frame that displays information about a reservation record, including book details, member information, and reservation dates.
    It also provides a button to delete the reservation record.
    """
    def __init__(self,parent, reservation : ReservationDTO, parent_page = None):
        super().__init__(parent)
        self.configure(fg_color="transparent")

        self.parent_page = parent_page
        self._book_service : BookService = BookService()
        self._exemplar_service : ExemplarService = ExemplarService()
        self._person_service : PersonService = PersonService()
        self._reservation_service : ReservationService = ReservationService()
        self._book = self._book_service.get_by_isbn(self._exemplar_service.get_by_id(reservation.id_exemplar).isbn)
        self._member = self._person_service.get_by_id(reservation.member.id_person)
        self.reservation = reservation

        self.tag_font = ctk.CTkFont(size=13, weight="bold")
        self.title_font = ctk.CTkFont(size=14, weight="bold")
        self.main_frame= ctk.CTkFrame(self,fg_color=Color.primary_color(),corner_radius=15)
        self.main_frame.pack(fill="x", padx=10,pady=5)

        
        self.label_reservation = ctk.CTkLabel(
            self.main_frame, 
            text=f"ID : {self.reservation.id_reservation}",
            corner_radius=25,
            height=25,
            fg_color=Color.secondary_color(),
            font = self.tag_font
        )
        self.label_reservation.pack(side="left", anchor="w", padx=(10,5), pady=10)

        self.label_book = ctk.CTkLabel(
            self.main_frame, 
            text=f"Book : {self._book.title}",
            corner_radius=25,
            height=25,
            fg_color=Color.background_color(),
            font = self.tag_font
        )
        self.label_book.pack(side="left", anchor="w", padx=(10,5), pady=10)

        self.label_member = ctk.CTkLabel(
            self.main_frame, 
            text=f"Member : {self._member.first_name} {self._member.last_name}",
            corner_radius=25,
            height=25,
            fg_color=Color.background_color(),
            font = self.tag_font
        )
        self.label_member.pack(side="left", anchor="w", padx=5, pady=10)
        if parent_page is not None:
            self.label_reservation_date = ctk.CTkLabel(
                self.main_frame, 
                text=f"Borrow date : {reservation.reservation_date}",
                corner_radius=25,
                height=25,
                fg_color=Color.background_color(),
                font = self.tag_font
            )
            self.label_reservation_date.pack(side="left", anchor="w", padx=5, pady=10)

            self.btn_delete = ctk.CTkButton(
                    self.main_frame,
                    text="🗑️ Delete",
                    width=100,
                    fg_color="transparent",
                    command=self.delete,
                    hover_color=(Color.hover_color(Color.error_color(), 30)),
                    border_width=2,
                    text_color="white",
                )
            self.btn_delete.pack(side="right", padx=(5, 10), pady=10)

    def delete(self):
        """
        Deletes the reservation record and removes the widget from the parent page.
        """
        try:
            self._reservation_service.delete_reservation(self.reservation.id_reservation)
        except Exception as e:
            PopUpMessage(self, f"{e}")