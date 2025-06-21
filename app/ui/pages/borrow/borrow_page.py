import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from services import BorrowService,BookService,ExemplarService,MemberService
from ui.components import PopUpMessage,SelectionFrame
from tools import Color
from .borrow_frame import BorrowFrame
class BorrowPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.borrow_service = BorrowService()
        self.book_service = BookService()
        self.exemplar_service = ExemplarService()
        self.member_service = MemberService()
        self.selected_borrow= None
        self.setup_ui()
        self.book_selected =[]
        self.member_selected = []
        self.paiement_type_selected = []

        

    def setup_ui(self):
        """
            Configure the user interface for the book management page.
            It sets up the search bar, scrollable book list, and information display.
        """
        
        self.grid_rowconfigure(2, weight=1) 
        self.grid_columnconfigure(0, weight=1)
        
        # === Search zone ===
        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        search_frame.grid_columnconfigure(0, weight=1)
        search_frame.grid_columnconfigure(1, weight=0) 
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search by title...",
            height=35
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        add_btn = ctk.CTkButton(
            search_frame,
            text="➕ ADD",
            fg_color=Color.primary_color(),
            height=35
        )
        add_btn.grid(row=0, column=2, padx=(5, 10), pady=10)
        
        
        
        
        # === Scrollable frame ===
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, scrollbar_button_color=Color.primary_color())
        self.scroll_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        # === Info ===
        info_frame = ctk.CTkFrame(self)
        info_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        self.info_label = ctk.CTkLabel(info_frame, text="", font=ctk.CTkFont(size=12))
        self.info_label.pack(pady=5)

    def on_search(self, event=None):
        """
            Handles the search functionality by filtering books based on the search query.
        """
        pass

    def load_borrow(self):
        pass