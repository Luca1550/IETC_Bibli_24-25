import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from services import BorrowService,BookService,ExemplarService,MemberService
from ui.components import PopUpMessage,SelectionFrame


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
        

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  

        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        

        self.form_title = ctk.CTkLabel(self.main_panel, text="Borrow", font=ctk.CTkFont(size=18, weight="bold"))
        self.form_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self.parambor = self.borrow_service.get_all()

        
        self.main_panel.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Configu 2 col
        self.main_panel.grid_columnconfigure(0, weight=1)
        self.main_panel.grid_columnconfigure(1, weight=2)
        self.main_panel.grid_rowconfigure(0, weight=1)

        self.left_panel = ctk.CTkFrame(self.main_panel)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.left_label = ctk.CTkLabel(self.left_panel, text="my borrow", font=ctk.CTkFont(size=16, weight="bold"))
        self.left_label.pack(pady=(10, 5))

        self.borrow_listbox = tk.Listbox(self.left_panel,  height=40)
        self.borrow_listbox.pack(expand=True, fill="both", padx=10, pady=10)

        

        self.right_panel = ctk.CTkFrame(self.main_panel)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        self.form_title = ctk.CTkLabel(self.right_panel, text="New Borrow", font=ctk.CTkFont(size=18, weight="bold"))
        self.form_title.pack(pady=(10, 10))
        self.title_entry = ctk.CTkEntry(self.right_panel, placeholder_text="title")
        self.title_entry.pack(pady=5, padx=20, fill="x")
        self.all_books= []
        for book in self.book_service.get_all():
            exemplars = self.exemplar_service.get_all_by_isbn(book.isbn)
            for exemplar in exemplars:
                if exemplar.status.value != 3 :
                    self.all_books.append(book)
                    break
        self.edit_book_button = ctk.CTkButton(self.right_panel, text="✏️", width=30, command=lambda:self.open_selection_frame(
            title="Book",
            all_items=self.all_books,
            selected_items=self.book_selected,
            display_model_method=lambda book: f"{book.title}",
            attributes_to_search=[lambda book: {book.title}],
            entry_to_update=self.title_entry
        ))
        self.member_entry = ctk.CTkEntry(self.right_panel, placeholder_text="Member")
        self.member_entry.pack(pady=5, padx=20, fill="x")
        self.edit_member_button = ctk.CTkButton(self.right_panel, text="✏️", width=30, command=lambda:self.open_selection_frame(
            title="Member",
            all_items=self.member_service.get_all_members(),
            selected_items=self.member_selected,
            display_model_method=lambda member: f"{member.person.first_name}",
            attributes_to_search=[lambda member: {member.person.first_name}],
            entry_to_update=self.member_entry
        ))
        #(self, isbn:str,id_member:int, borrow_date:date|None,paiement_type:int,paiement_status:int):
        self.borrow_date = ctk.CTkEntry(self.right_panel, placeholder_text="Date (YYYY-MM-DD)")
        self.borrow_date.pack(pady=5, padx=20, fill="x")
        self.paiement_type = ctk.CTkEntry(self.right_panel, placeholder_text="Date (YYYY-MM-DD)")
        self.paiement_type.pack(pady=5, padx=20, fill="x")
        self.edit_paiement_type_button = ctk.CTkButton(self.right_panel, text="✏️", width=30, command=lambda:self.open_selection_frame(
            title="paiement type",
            all_items=self.paiement_type_enum.paiement_type(),
            selected_items=self.paiement_type_selected,
            display_model_method=lambda member: f"{member.person.first_name}",
            attributes_to_search=[lambda member: {member.person.first_name}],
            entry_to_update=self.member_entry
        ))
        self.edit_book_button.pack(pady=(10, 10))
        self.edit_member_button.pack(pady=(10, 10))
        self.edit_member_button.pack(pady=(10, 10))
        self.submit_button = ctk.CTkButton(self.right_panel, text="Réserver",command=self.add_reservation)
        self.submit_button.pack(pady=20)
    def add_reservation(self):
        try:
            title = self.title_entry.get()
            id_exemplar = self.reservation_service.get_exemplar_by_name(title)
            if id_exemplar is None:
                PopUpMessage.pop_up(self, "Exemplar not found for the given title.")
                return
            id_member = int(self.member_entry.get())
            reservation_date = str(self.date_entry.get())
            newreservation=self.reservation_service.add_reservation(id_exemplar,id_member,reservation_date)
            if isinstance(newreservation, str):
                PopUpMessage.pop_up(self, newreservation)
            else:
                PopUpMessage.pop_up(self, "reservation added successfully!")
                self.destroy()
            self.submit_button.configure(text="Réserver", command=self.add_reservation)

        except ValueError as e:
            PopUpMessage.pop_up(self, f"Input error: {e}")