import customtkinter as ctk
from tools import Color
from services import MemberService, BorrowService, ReservationService, BookService, ThemeService, EditorService, AuthorService, CollectionService, LibraryService
from ui.pages.borrow import BorrowFrame
from ui.pages.reservation import ReservationFrame
from datetime import datetime, date

class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self._member_service : MemberService = MemberService()
        self._member_data = self._member_service.get_all_members()
        self._book_service : BookService = BookService()
        self._book_data = self._book_service.get_all()
        self._theme_service : ThemeService = ThemeService()
        self._theme_data = self._theme_service.get_all()
        self._editor_service : EditorService = EditorService()
        self._editor_data = self._editor_service.get_all()
        self._author_service : AuthorService = AuthorService()
        self._author_data = self._author_service.get_all()
        self._collection_service : CollectionService = CollectionService()
        self._collection_data = self._collection_service.get_all()
        self._library_service : LibraryService = LibraryService()
        self._borrow_service : BorrowService = BorrowService()
        self._borrow_data = [borrow for borrow in self._borrow_service.get_all() if datetime.fromisoformat(borrow.return_date).date() == date.today()]
        self._reservation_service : ReservationService = ReservationService()
        self._reservation_data = [reservation for reservation in self._reservation_service.get_all() if datetime.fromisoformat(reservation.reservation_date).date() == date.today()]
        self._library_data = self._library_service.get_library_parameters()[0] if self._library_service.get_library_parameters()[0] is not None else []

# region frame
        self.grid_rowconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.reservation_today_frame = ctk.CTkFrame(self, border_color=Color.primary_color(), border_width=5, corner_radius=5)
        self.reservation_today_frame.grid(row=0, column=0, columnspan=2, padx=(10, 5), pady=(10, 5), sticky="nsew")
        self.borrowed_today_frame = ctk.CTkFrame(self, border_color=Color.primary_color(), border_width=5, corner_radius=5)
        self.borrowed_today_frame.grid(row=0, column=2, columnspan=2, padx=(5, 10), pady=(10, 5), sticky="nsew")
        
        self.stat_members_frame = ctk.CTkFrame(self, border_color=Color.primary_color(), border_width=5, corner_radius=5)
        self.stat_members_frame.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky="nsew")

        self.stat_books_frame = ctk.CTkFrame(self, border_color=Color.primary_color(), border_width=5, corner_radius=5)
        self.stat_books_frame.grid(row=1, column=1, columnspan=2, padx=5, pady=(5, 10), sticky="nsew")  # occupe 2 colonnes ici

        self.prices_frame = ctk.CTkFrame(self, border_color=Color.primary_color(), border_width=5, corner_radius=5)
        self.prices_frame.grid(row=1, column=3, padx=(5, 10), pady=(5, 10), sticky="nsew")

# endregion

# region stat_members
        self.stat_members_title = ctk.CTkLabel(self.stat_members_frame, bg_color=Color.primary_color(),corner_radius=5,text="Members Statitics", font=ctk.CTkFont(weight='bold', size=14))
        self.stat_members_title.pack(fill="x", padx=5, pady=(5, 10))
        self.stat_members_nb_members = ctk.CTkLabel(self.stat_members_frame, bg_color="transparent", corner_radius=5, fg_color="transparent",text=f"✅ {len(self._member_data)} members")
        self.stat_members_nb_members.pack(fill="x", padx=5)
        divider(self.stat_members_frame)
        self.stat_members_nb_subscribed = ctk.CTkLabel(self.stat_members_frame, bg_color="transparent", corner_radius=5, fg_color="transparent",text=f"💲 {len([member for member in self._member_data if member.subscribed])} subscribed members")
        self.stat_members_nb_subscribed.pack(fill="x", padx=5)
# endregion

# region stat_books
        self.stat_books_title = ctk.CTkLabel(self.stat_books_frame, bg_color=Color.primary_color(),corner_radius=5, text="Books Statitics", font=ctk.CTkFont(weight='bold', size=14))
        self.stat_books_title.pack(fill="x", padx=5, pady=(5, 10))
        self.stat_books_nb_books = ctk.CTkLabel(self.stat_books_frame,  bg_color="transparent", corner_radius=5, fg_color="transparent", text=f"📖 {len(self._book_data)} books")
        self.stat_books_nb_books.pack(fill="x", padx=10)
        divider(self.stat_books_frame)
        self.stat_books_nb_authors = ctk.CTkLabel(self.stat_books_frame, bg_color="transparent", corner_radius=5, fg_color="transparent", text=f"✍️ {len(self._author_data)} authors")
        self.stat_books_nb_authors.pack(fill="x", padx=10)
        divider(self.stat_books_frame)
        self.stat_books_nb_themes = ctk.CTkLabel(self.stat_books_frame,  bg_color="transparent", corner_radius=5, fg_color="transparent", text=f"🧩 {len(self._theme_data)} themes")
        self.stat_books_nb_themes.pack(fill="x", padx=10)
        divider(self.stat_books_frame)
        self.stat_books_nb_collection = ctk.CTkLabel(self.stat_books_frame,  bg_color="transparent", corner_radius=5, fg_color="transparent", text=f"📚 {len(self._collection_data)} collections")
        self.stat_books_nb_collection.pack(fill="x", padx=10)
        divider(self.stat_books_frame)
        self.stat_books_nb_editors = ctk.CTkLabel(self.stat_books_frame,  bg_color="transparent", corner_radius=5, fg_color="transparent", text=f"🏢 {len(self._editor_data)} editors")
        self.stat_books_nb_editors.pack(fill="x", padx=10)
# endregion

# region prices
        self.prices_title = ctk.CTkLabel(self.prices_frame, text="Prices",bg_color=Color.primary_color(), corner_radius=5,font=ctk.CTkFont(weight='bold', size=14))
        self.prices_title.pack(fill="x", padx=5, pady=(5, 10))
        self.prices_subscribe_amout = ctk.CTkLabel(self.prices_frame, bg_color="transparent", corner_radius=5, fg_color="transparent",text=f"Subscribe : {self._library_data.subscribe_amout if self._library_data else "None"} €")
        self.prices_subscribe_amout.pack(fill="x", padx=10)
        divider(self.prices_frame)
        self.prices_borrow_price_with_sub = ctk.CTkLabel(self.prices_frame,  bg_color="transparent", corner_radius=5, fg_color="transparent", text=f"Borrow price with sub : {self._library_data.borrow_price_with_sub if self._library_data else "None"} €")
        self.prices_borrow_price_with_sub.pack(fill="x", padx=10)
        divider(self.prices_frame)
        self.prices_borrow_price_without_sub = ctk.CTkLabel(self.prices_frame,  bg_color="transparent", corner_radius=5, fg_color="transparent", text=f"Borrow price without sub : {self._library_data.borrow_price_without_sub if self._library_data else "None"} €")
        self.prices_borrow_price_without_sub.pack(fill="x", padx=10)
# endregion

# region reservation_today
        self.reservation_today_title = ctk.CTkLabel(self.reservation_today_frame, bg_color=Color.primary_color(),corner_radius=5,text="Reservation Today", font=ctk.CTkFont(weight='bold', size=14))
        self.reservation_today_title.pack(fill="x",padx=5, pady=(5, 10))
        self.reservation_today_scroll_frame = ctk.CTkScrollableFrame(self.reservation_today_frame, scrollbar_button_color=Color.primary_color())
        self.reservation_today_scroll_frame.pack(fill="both", expand=True, padx=12.5, pady=(0,12.5))
        if self._reservation_data:
            for reservation in self._reservation_data:
                self.reservation_frame = ReservationFrame(
                self.reservation_today_scroll_frame,
                reservation
                )
                self.reservation_frame.pack(fill="x", pady=5)
        else:
            self.no_reservation_label = ctk.CTkLabel(self.reservation_today_scroll_frame, text="No reservation today")
            self.no_reservation_label.pack(fill="x", pady=5)
# endregion

# region borrowed_today
        self.borrowed_today_title = ctk.CTkLabel(self.borrowed_today_frame,bg_color=Color.primary_color(),corner_radius=5, text="Borrowed Today", font=ctk.CTkFont(weight='bold', size=14))
        self.borrowed_today_title.pack(fill="x",padx=5, pady=(5, 10))
        self.borrowed_today_scroll_frame = ctk.CTkScrollableFrame(self.borrowed_today_frame, scrollbar_button_color=Color.primary_color())
        self.borrowed_today_scroll_frame.pack(fill="both", expand=True, padx=12.5, pady=(0,12.5))
        if self._borrow_data:
            for borrow in self._borrow_data:
                self.borrow_frame = BorrowFrame(
                self.borrowed_today_scroll_frame,
                borrow
                )
                self.borrow_frame.pack(fill="x", pady=5)
        else:
            self.no_borrow_label = ctk.CTkLabel(self.borrowed_today_scroll_frame, text="No borrowed today")
            self.no_borrow_label.pack(fill="x", pady=5)
# endregion

def divider(frame):
    divider = ctk.CTkFrame(frame, height=2, fg_color="gray", bg_color="transparent")
    divider.pack(fill="x", padx=10, pady=2)