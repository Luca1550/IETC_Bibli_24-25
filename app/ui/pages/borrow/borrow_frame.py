import customtkinter as ctk
from tools import Color
from services.models import BorrowDTO
from services import ExemplarService, BookService, PersonService, BorrowService
from ui.components import PopUpMessage
class BorrowFrame(ctk.CTkFrame):
    
    
    def __init__(self,parent, borrow : BorrowDTO, parent_page):
        super().__init__(parent)
        self.parent_page = parent_page
        self._book_service : BookService = BookService()
        self._exemplar_service : ExemplarService = ExemplarService()
        self._person_service : PersonService = PersonService()
        self._borrow_service : BorrowService = BorrowService()
        self._book = self._book_service.get_by_isbn(self._exemplar_service.get_by_id(borrow.id_exemplar).isbn)
        self._member = self._person_service.get_by_id(borrow.member.id_person)
        self.borrow = borrow

        self.tag_font = ctk.CTkFont(size=13, weight="bold")
        self.title_font = ctk.CTkFont(size=14, weight="bold")
        self.main_frame= ctk.CTkFrame(self,fg_color=Color.primary_color(),corner_radius=15)
        self.main_frame.pack(fill="x", padx=10,pady=5)

        
        self.label_book = ctk.CTkLabel(
            self.main_frame, 
            text=f"Book : {self._book.isbn} | {self._book.title}",
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

        self.label_borrow_date = ctk.CTkLabel(
            self.main_frame, 
            text=f"Borrow date : {borrow.borrow_date}",
            corner_radius=25,
            height=25,
            fg_color=Color.background_color(),
            font = self.tag_font
        )
        self.label_borrow_date.pack(side="left", anchor="w", padx=5, pady=10)

        self.label_return_date = ctk.CTkLabel(
            self.main_frame, 
            text=f"Return date : {borrow.return_date}",
            corner_radius=25,
            height=25,
            fg_color=Color.background_color(),
            font = self.tag_font
        )
        self.label_return_date.pack(side="left", anchor="w", padx=5, pady=10)

        self.btn_delete = ctk.CTkButton(
                self.main_frame,
                text="❎ Delete",
                width=100,
                fg_color="transparent",
                command=self.delete,
                hover_color=(Color.hover_color(Color.error_color(), 30)),
                border_width=2,
                text_color="white",
            )
        self.btn_delete.pack(side="right", padx=(5, 10), pady=10)

    def delete(self):
        try:
            self._borrow_service.delete_borrow(self.borrow.id_borrow)
            self.parent_page.all_items_widgets[self.borrow.id_borrow].destroy()
        except Exception as e:
            PopUpMessage(self, f"{e}")