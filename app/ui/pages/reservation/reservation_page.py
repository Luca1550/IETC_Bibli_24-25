
import customtkinter as ctk
import tkinter as tk
from services import ReservationService,BookService,ExemplarService,MemberService,PersonService,BorrowService
from ui.components import PopUpMessage,SelectionFrame
from datetime import date 
from datetime import datetime



class ReservationPage(ctk.CTkFrame):
    """
    Page for managing reservations.
    This class provides a user interface for creating and updating reservations.
    It allows users to select books and members, enter reservation dates, and submit or update reservations."""

    def __init__(self, parent):
        """
        Initializes the ReservationPage with the given parent widget.
        """
        super().__init__(parent)
        self.reservation_service = ReservationService()
        self.book_service = BookService()
        self.exemplar_service = ExemplarService()
        self.member_service = MemberService()
        self.personne_servce= PersonService()
        self.borrow_service = BorrowService()
        self.selected_reservation= None
        self.setup_ui()
        self.book_selected =[]
        self.member_selected=[]
    def setup_ui(self):
        """Sets up the user interface for the reservation page.
        This method creates the main layout, including the title, listbox for reservations, and form for adding or updating reservations."""

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  

        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        

        self.form_title = ctk.CTkLabel(self.main_panel, text="Rerservation", font=ctk.CTkFont(size=18, weight="bold"))
        self.form_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self.paramres = self.reservation_service.get_all()

        
        self.main_panel.grid_columnconfigure(0, weight=1)
        self.main_panel.grid_columnconfigure(1, weight=2)
        self.main_panel.grid_rowconfigure(0, weight=1)

        self.left_panel = ctk.CTkFrame(self.main_panel)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.left_label = ctk.CTkLabel(self.left_panel, text="Reservation", font=ctk.CTkFont(size=16, weight="bold"))
        self.left_label.pack(pady=(10, 5))

        self.reservation_listbox = tk.Listbox(self.left_panel,  height=40, bg="#2b2b2b",fg="white",highlightthickness=0,bd=0,relief="flat",selectbackground="#444",selectforeground="white" )
        self.reservation_listbox.pack(expand=True, fill="both", padx=10, pady=10)

        self.paramres = self.reservation_service.get_all()
        self.indexbook = {}
        for idx,res in enumerate(self.paramres):

            member_firstname=self.personne_servce.get_by_id(res.member.id_person).first_name if res.member else "Inconnu"
            member_name=self.personne_servce.get_by_id(res.member.id_person).last_name if res.member else "Inconnu"
            paramexemplar=self.exemplar_service.get_by_id(res.id_exemplar)
            titleisbn =self.book_service.get_by_isbn(paramexemplar.isbn)
            title=titleisbn.title
            self.reservation_listbox.insert("end", f"{res.reservation_date} | title: {title} | Membre: {member_firstname} {member_name}")
            self.indexbook[idx] = res
        self.reservation_listbox.bind("<<ListboxSelect>>", self.reservation_select)
        self.add_page()

    def add_page(self):
        self.right_panel = ctk.CTkFrame(self.main_panel)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        self.form_title = ctk.CTkLabel(self.right_panel, text="Add reservation", font=ctk.CTkFont(size=18, weight="bold"))
        self.form_title.pack(pady=(10, 10))
        self.book_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.book_frame.pack(pady=5, padx=20, fill="x")
        self.member_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.member_frame.pack(pady=5, padx=20, fill="x")
        self.book_entry = ctk.CTkEntry(self.book_frame, placeholder_text="title")
        self.book_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.all_books= []
        for book in self.book_service.get_all():
            exemplars = self.exemplar_service.get_all_by_isbn(book.isbn)
            for exemplar in exemplars:
                if exemplar.status.value != 3 and not exemplar.id in ([res.id_exemplar for res in self.indexbook.values()]):
                    self.all_books.append(book)
                    break
        self.edit_book_button = ctk.CTkButton(self.book_frame, text="✏️", width=30, command=lambda:self.open_selection_frame(
            title="Book",
            all_items=self.all_books,
            selected_items=self.book_selected,
            display_model_method=lambda book: f"{book.title}",
            attributes_to_search=[lambda book: {book.title}],
            entry_to_update=self.book_entry
        ))
        self.member_entry = ctk.CTkEntry(self.member_frame, placeholder_text="Member")
        self.member_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        self.edit_member_button = ctk.CTkButton(self.member_frame, text="✏️", width=30, command=lambda:self.open_selection_frame(
            title="Member",
            all_items=self.member_service.get_all_members(),
            selected_items=self.member_selected,
            display_model_method=lambda member: f"{member.person.first_name} {member.person.last_name }",
                attributes_to_search=[lambda member: member.person.first_name, lambda member:member.person.last_name],
            entry_to_update=self.member_entry
        ))
        self.date_entry = ctk.CTkEntry(self.right_panel, placeholder_text="Date (YYYY-MM-DD)")
        self.date_entry.pack(pady=5, padx=20, fill="x")

        self.edit_book_button.pack(side="left")
        
        self.edit_member_button.pack(side="left")
        
        self.submit_button = ctk.CTkButton(self.right_panel, text="Add",command=self.add_reservation)
        self.submit_button.pack(pady=20)
        
    def add_reservation(self):
        """Handles the addition of a new reservation.
        This method retrieves the selected book and member, validates the reservation date,
        and calls the reservation service to add the reservation.
        If the reservation is successfully added, it refreshes the listbox and clears the form."""
        try:
            if len(self.member_selected) ==1:
                id_member= self.member_selected[0].id_member
            else:
                PopUpMessage.pop_up(self, "More than one member")
                return 

            if not len(self.book_selected) ==1:
                PopUpMessage.pop_up(self, "More than one exemplar")
                return 
            
            
            if datetime.fromisoformat(self.date_entry.get()) > datetime.fromisoformat(date.today().isoformat()):
                reservation_date = str(self.date_entry.get())
            else:
                PopUpMessage.pop_up(self, "Wrong date")
                return
            newreservation=self.reservation_service.add_reservation(self.book_selected[0].isbn,id_member,reservation_date)
            if isinstance(newreservation, str):
                PopUpMessage.pop_up(self, newreservation)
            else:
                PopUpMessage.pop_up(self, "reservation added successfully!")
                self.refresh_listbox()
                self.clear_form_add()
                self.add_page()
        except ValueError as e:
            PopUpMessage.pop_up(self, f"Input error: {e}")

    def update_reservation(self):
        """Handles the update of an existing reservation.
        This method retrieves the selected book and member, validates the reservation date,
        and calls the reservation service to update the reservation.
        If the reservation is successfully updated, it refreshes the listbox and clears the form."""
        try:
            if len(self.member_selected) ==1:
                id_member= self.member_selected[0].id_member
            else:
                PopUpMessage.pop_up(self, "More than one exemplar")
                return 

            if datetime.fromisoformat(self.date_entry.get()) > datetime.fromisoformat(date.today().isoformat()):
                reservation_date = str(self.date_entry.get())
            else:
                PopUpMessage.pop_up(self, "Wrong date")
                return
            newreservation=self.reservation_service.update_reservation(self.id_reservation,id_member,reservation_date)
            if isinstance(newreservation, str):
                PopUpMessage.pop_up(self, newreservation)
            else:
                PopUpMessage.pop_up(self, "reservation updated successfully!")
                self.refresh_listbox()
                self.clear_form_up_del()
                self.add_page()

        except ValueError as e:
            PopUpMessage.pop_up(self, f"Input error: {e}")

    def delete_reservation(self):
        """Handles the deletion of an existing reservation.
        This method calls the reservation service to delete the reservation by its ID."""
        try:

            delreservation=self.reservation_service.delete_reservation(self.id_reservation)
            if isinstance(delreservation, str):
                PopUpMessage.pop_up(self, delreservation)
            else:
                PopUpMessage.pop_up(self, "reservation deleted successfully!")
                self.refresh_listbox()
                self.clear_form_up_del()
                self.add_page()
        except ValueError as e:
            PopUpMessage.pop_up(self, f"Input error: {e}")
    def reservation_select(self, event):
        """Handles the selection of a reservation from the listbox.
        This method retrieves the selected reservation, clears the form, and populates it with the selected reservation's details.
        It allows the user to update or delete the reservation."""
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_res = self.indexbook.get(index)
            for widget in [getattr(self, name, None) for name in ["book_frame", "member_frame", "title_entry","book_entry","member_entry","date_entry", "edit_book_button", "edit_member_button", "form_title", "button_frame", "submit_button", "delete_button"]]:
                if widget:
                    widget.destroy()
            
            
            self.form_title = ctk.CTkLabel(self.right_panel, text="Update Reservation", font=ctk.CTkFont(size=18, weight="bold"))
            self.form_title.pack(pady=(10, 10))
            self.member_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
            self.member_frame.pack(pady=5, padx=20, fill="x")

            self.member_entry = ctk.CTkEntry(self.member_frame, placeholder_text="Member")
            self.member_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
            
            
            self.date_entry = ctk.CTkEntry(self.right_panel, placeholder_text="reservation_date")
            self.date_entry.pack(pady=5, padx=20, fill="x")
            
            self.button_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
            self.button_frame.pack(pady=20, fill="x", padx=20)

            self.button_frame.grid_columnconfigure(0, weight=1)
            self.button_frame.grid_columnconfigure(1, weight=1)

            self.submit_button = ctk.CTkButton(self.button_frame, text="Update", command=self.update_reservation)
            self.submit_button.pack(side="right", expand=True, padx=10)

            self.borrow_button = ctk.CTkButton(self.button_frame, text="Borrow this reservation")
            self.borrow_button.pack(side="right", expand=True, padx=10)

            self.delete_button = ctk.CTkButton(self.button_frame, text="Delete", command=self.delete_reservation)
            self.delete_button.pack(side="left", expand=True, padx=10)

            if selected_res:
                self.id_reservation=selected_res.id_reservation
                self.selected_reservation = selected_res
                self.member_selected.append(self.member_service.get_member_by_id(selected_res.member.id))
                
                    
                self.edit_member_button = ctk.CTkButton(self.member_frame, text="✏️", width=30, command=lambda:self.open_selection_frame(
                title="Member",
                all_items=self.member_service.get_all_members(),
                selected_items=self.member_selected,
                display_model_method=lambda member: f"{member.person.first_name} {member.person.last_name }",
                attributes_to_search=[lambda member: member.person.first_name, lambda member:member.person.last_name],
                entry_to_update=self.member_entry
                ))
                self.borrow_button.configure(command= lambda: self.borrow(selected_res.member, selected_res.id_exemplar, selected_res.id_reservation))
                self.edit_member_button.pack(side='left')
                self.member_entry.insert(0, self.member_selected[0].person.first_name)
                self.date_entry.insert(0, selected_res.reservation_date)
        
    def open_selection_frame(self,title,all_items,selected_items,display_model_method,attributes_to_search,entry_to_update,attributes_to_entry=None):
        """Opens a selection frame for choosing items from a list.
        This method creates a SelectionFrame instance and waits for it to close before proceeding."""
        selection_frame = SelectionFrame(
            self,
            title,
            all_items,
            selected_items,
            display_model_method,
            attributes_to_search,
            entry_to_update,
            attributes_to_entry
        )
        self.wait_window(selection_frame)


    def refresh_listbox(self):
        """Refreshes the listbox of reservations.
        This method clears the current listbox, retrieves all reservations from the reservation service, and populates the listbox with the updated data."""
        self.reservation_listbox.delete(0, tk.END)  
        self.paramres = self.reservation_service.get_all()  
        self.indexbook = {}

        self.paramres = self.reservation_service.get_all()
        self.indexbook = {}
        for idx,res in enumerate(self.paramres):

            member_firstname=self.personne_servce.get_by_id(res.member.id_person).first_name if res.member else "unknown"
            member_name=self.personne_servce.get_by_id(res.member.id_person).last_name if res.member else "unknown"
            paramexemplar=self.exemplar_service.get_by_id(res.id_exemplar)
            titleisbn =self.book_service.get_by_isbn(paramexemplar.isbn)
            title=titleisbn.title
            self.reservation_listbox.insert("end", f"{res.reservation_date} | title: {title} | Membre: {member_firstname} {member_name}")
            self.indexbook[idx] = res

    def clear_form_add(self):
        """Clears the form fields for adding a new reservation.
        This method resets the title, member, and date entries, and clears the selected book and member lists."""
        self.book_entry.configure(state="normal")
        self.member_entry.configure(state="normal")
        self.book_entry.delete(0, tk.END)
        self.member_entry.delete(0, tk.END)
        self.member_entry.configure(state="disabled")
        self.book_entry.configure(state="disabled")
        self.date_entry.delete(0, tk.END)
        self.book_selected.clear()
        self.member_selected.clear()
        

    def clear_form_up_del(self):
        self.member_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.member_selected.clear()

    def borrow(self, member, id_exemplar : int, id_reservation : int):
        try:
            self.borrow_service.add_borrow(None, member.id, id_exemplar, id_reservation)
            PopUpMessage.pop_up(self, "Borrow added successfully!")
            self.refresh_listbox()
            self.add_page()
        except Exception as e:
            PopUpMessage.pop_up(self, f"{e}")
        
        
