import customtkinter as ctk
from services import BorrowService,BookService,ExemplarService,MemberService
from tools import Color
from .borrow_add_page import BorrowAddPage
from .borrow_frame import BorrowFrame

class BorrowPage(ctk.CTkFrame):
    """
    A page for managing borrow records in the library system.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.borrow_service = BorrowService()
        self.book_service = BookService()
        self.exemplar_service = ExemplarService()
        self.member_service = MemberService()
        self.selected_borrow= None
        self.borrow_list = self.borrow_service.get_all()
        self.filtered_borrow = self.borrow_list.copy()
        self.all_items_widgets : dict[str, ctk.CTkFrame] = {}
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface for the borrow page.
        It includes a search entry, an add button, and a scrollable frame to display borrow records.
        """
        
        self.grid_rowconfigure(2, weight=1) 
        self.grid_columnconfigure(0, weight=1)

        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        search_frame.grid_columnconfigure(0, weight=1)
        search_frame.grid_columnconfigure(1, weight=0) 
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search by id...",
            height=35
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        add_btn = ctk.CTkButton(
            search_frame,
            text="➕ ADD",
            command=self.open_borrow_add_page,
            fg_color=Color.primary_color(),
            height=35
        )
        add_btn.grid(row=0, column=2, padx=(5, 10), pady=10)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, scrollbar_button_color=Color.primary_color())
        self.scroll_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))
        self.load_borrow()

    def open_borrow_add_page(self):
        """
        Opens the borrow add page to allow the user to add a new borrow record.
        """
        borrow_add_page = BorrowAddPage()
        self.wait_window(borrow_add_page)
        self.borrow_list = self.borrow_service.get_all()
        self.filtered_borrow = self.borrow_list.copy()
        self.load_borrow()

    def on_search(self, event=None):
        """
        Handles the search functionality.
        It filters the borrow records based on the search query entered by the user.
        """
        query = self.search_entry.get().lower().strip()
        if not query:
            self.filtered_borrow = self.borrow_list.copy()
        else:
            self.filtered_borrow = [
                borrow for borrow in self.borrow_list
                if query in str(borrow.id_borrow) or
                query in self.member_service.get_member_by_id(borrow.member.id).person.first_name.lower() or
                query in self.member_service.get_member_by_id(borrow.member.id).person.last_name.lower() 
            ]
        
        self.load_borrow()

    def load_borrow(self):
        """
        Loads the borrow records into the scrollable frame.
        It creates or updates the BorrowFrame widgets for each borrow record.
        It also filters the records based on the search query.
        """

        filtered_ids = {borrow.id_borrow for borrow in self.filtered_borrow}
        for id_borrow, widget in self.all_items_widgets.items():
            if id_borrow in filtered_ids:
                widget.pack(fill="x", padx=(0, 10), pady=5)
            else:
                widget.pack_forget()

        for borrow in self.filtered_borrow:
            if borrow.id_borrow not in self.all_items_widgets:
                borrow_frame = BorrowFrame(
                    self.scroll_frame,
                    borrow,
                    self,
                )
                borrow_frame.pack(fill="x", padx=5, pady=5)
                self.all_items_widgets[borrow.id_borrow] = borrow_frame
