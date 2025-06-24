import customtkinter as ctk
import os
from services import MemberService, ExemplarService,PaymentService
from ui.components import PopUpMessage
import datetime
from datetime import datetime
from tools import Color

class MemberPage(ctk.CTkFrame):
    """
    MemberPage class that manages the member management interface.
    It allows adding, deleting, and displaying members.
    """
    def __init__(self, parent, **kwargs):
        """
        Initializes the MemberPage class and sets up the UI components.
        """
        super().__init__(parent, **kwargs)
        self.member_service = MemberService()
        self.exemplar_service = ExemplarService()
        self.members = self.member_service.get_all_members()
        self.payment_service= PaymentService()
        self.setup_ui()
        

    def setup_ui(self):
        """
        Sets up the UI components for the MemberPage.
        """
        rows = 1
        rows_weights = [1]
        columns = 2
        columns_weights = [1,5]

        for row, w in enumerate(rows_weights):
            self.grid_rowconfigure(row, weight=w)

        for column, w in enumerate(columns_weights):
            self.grid_columnconfigure(column, weight=w)

        self.member_frame = ctk.CTkFrame(self)
        self.member_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.member_frame.grid_rowconfigure(0, weight=0)
        self.member_frame.grid_rowconfigure(1, weight=1)
        self.member_frame.grid_columnconfigure(0, weight=1)
        self.member_frame.grid_columnconfigure(1, weight=0)

        self.search_bar_frame = ctk.CTkFrame(self.member_frame)
        self.search_bar_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.search_bar_frame.grid_columnconfigure(0, weight=1)
        self.search_bar_frame.grid_columnconfigure(1, weight=0)

        self.search_bar = ctk.CTkEntry(
            self.search_bar_frame,
            placeholder_text="Search Member",
            width=200
        )
        self.search_bar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.search_bar.bind("<KeyRelease>", self.filter_members)

        self.add_member_button = ctk.CTkButton(
            self.search_bar_frame,
            text="➕",
            command=self.add_member,
            width=40,
            height=40,
        )
        self.add_member_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.member_list_frame = ctk.CTkScrollableFrame(
            self.member_frame
        )
        self.member_list_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.display_members()

        self.borrows_by_member_frame = ctk.CTkScrollableFrame(self)
        self.borrows_by_member_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    def filter_members(self, event=None):
        query = self.search_bar.get().lower() 

        all_members = self.member_service.get_all_members()

        filtered_members = [
            m for m in all_members
            if (
                (query in m.person.first_name.lower() or
                query in m.person.last_name.lower() or
                query in m.person.street.lower() or
                query in m.person.city.lower() or
                query in m.person.cp.lower() or
                query in str(m.id_member))
                
            )
        ]

        self.display_members(filtered_members)

    def display_members(self, members=None):
        """
        Displays the list of members in the right-side frame.
        """

        for widget in self.member_list_frame.winfo_children():
            widget.destroy()

        self.member_service = MemberService()

        if members is None:
            members = self.member_service.get_all_members()

        if members:
            row_index = 0
            for member in members:
                id_label = ctk.CTkLabel(
                    self.member_list_frame,
                    text=f"ID: {member.id_member}",
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                id_label.grid(row=row_index, column=0, sticky="w", padx=15, pady=(5, 0))
                row_index += 1

                last_name_label = ctk.CTkLabel(
                    self.member_list_frame,
                    text=f"Last name: {member.person.last_name}",
                    font=ctk.CTkFont(size=16)
                )
                last_name_label.grid(row=row_index, column=0, sticky="w", padx=15)
                row_index += 1

                first_name_label = ctk.CTkLabel(
                    self.member_list_frame,
                    text=f"First name: {member.person.first_name}",
                    font=ctk.CTkFont(size=16)
                )
                first_name_label.grid(row=row_index, column=0, sticky="w", padx=15)
                row_index += 1

                address_label = ctk.CTkLabel(
                    self.member_list_frame,
                    text=f"Address: {member.person.street}, {member.person.cp} ,{member.person.city}",
                    font=ctk.CTkFont(size=16)
                )
                address_label.grid(row=row_index, column=0, sticky="w", padx=15)
                row_index += 1

                subscribed_label = ctk.CTkLabel(
                    self.member_list_frame,
                    text=f"Subscribed: {'Yes' if member.subscribed else 'No'}",
                    font=ctk.CTkFont(size=16)
                )
                subscribed_label.grid(row=row_index, column=0, sticky="w", padx=15)
                row_index += 1

                edit_button = ctk.CTkButton(
                    self.member_list_frame,
                    text="Edit",
                    command=lambda m_id=member.id_member: self.update_member(m_id), 
                    width=80
                )
                edit_button.grid(row=row_index, column=0, sticky="w", padx=10, pady=(0, 10))
                row_index += 1
                
                show_borrowed_books_button = ctk.CTkButton(
                    self.member_list_frame,
                    text="Show Borrowed Books",
                    command=lambda m_id=member.id_member: self.display_borrows_by_member(m_id),
                    width=160
                )
                show_borrowed_books_button.grid(row=row_index, column=0, sticky="w", padx=10, pady=(0, 10))
                row_index += 1

                delete_button = ctk.CTkButton(
                    self.member_list_frame,
                    text="Delete",
                    command=lambda m_id=member.id_member: self.delete_member(m_id),
                    width=240,
                    fg_color=Color.secondary_color(),
                    hover_color=Color.error_color()
                )
                delete_button.grid(row=row_index, column=0, sticky="w", padx=10, pady=(0, 10))
                row_index += 1
                
        else:
            no_members_label = ctk.CTkLabel(
                self.member_list_frame,
                text="No members found.",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            no_members_label.grid(row=0, column=0, padx=15, pady=(5, 0))

    def add_member(self):
        """
        Opens a dialog to add a new member and updates the display.
        """
        self.add_member_frame = ctk.CTkToplevel(self)
        self.add_member_frame.geometry("400x600")
        self.add_member_frame.title("ADD MEMBER")
        self.add_member_frame.focus_set()
        self.add_member_frame.grab_set()
        self.add_member_frame.lift()

        rows = 17
        rows_weights = [1]*rows
        columns = 1
        columns_weights = [1]

        for row, w in enumerate(rows_weights):
            self.add_member_frame.grid_rowconfigure(row, weight=w)

        for column, w in enumerate(columns_weights):
            self.add_member_frame.grid_columnconfigure(column, weight=w)

        self.first_name_label = ctk.CTkLabel(self.add_member_frame, text="First Name")
        self.first_name_label.grid(row=0, column=0, padx=10, pady=0, sticky="w")
        self.first_name_entry = ctk.CTkEntry(self.add_member_frame, placeholder_text="First Name")
        self.first_name_entry.grid(row=1, column=0, padx=10, pady=0, sticky="ew")
        self.first_name_entry.focus_set()

        self.last_name_label = ctk.CTkLabel(self.add_member_frame, text="Last Name")
        self.last_name_label.grid(row=2, column=0, padx=10, pady=0, sticky="w")
        self.last_name_entry = ctk.CTkEntry(self.add_member_frame, placeholder_text="Last Name")
        self.last_name_entry.grid(row=3, column=0, padx=10, pady=0, sticky="ew")

        self.national_number_label = ctk.CTkLabel(self.add_member_frame, text="National Number")
        self.national_number_label.grid(row=4, column=0, padx=10, pady=0, sticky="w")
        self.national_number_entry = ctk.CTkEntry(self.add_member_frame, placeholder_text="National Number")
        self.national_number_entry.grid(row=5, column=0, padx=10, pady=0, sticky="ew")

        self.email_label = ctk.CTkLabel(self.add_member_frame, text="Email")
        self.email_label.grid(row=6, column=0, padx=10, pady=0, sticky="w")
        self.email_entry = ctk.CTkEntry(self.add_member_frame, placeholder_text="Email")
        self.email_entry.grid(row=7, column=0, padx=10, pady=0, sticky="ew")

        self.street_label = ctk.CTkLabel(self.add_member_frame, text="Street")
        self.street_label.grid(row=8, column=0, padx=10, pady=0, sticky="w")
        self.street_entry = ctk.CTkEntry(self.add_member_frame, placeholder_text="Street")
        self.street_entry.grid(row=9, column=0, padx=10, pady=0, sticky="ew")

        self.cp_label = ctk.CTkLabel(self.add_member_frame, text="Postal Code")
        self.cp_label.grid(row=10, column=0, padx=10, pady=0, sticky="w")
        self.cp_entry = ctk.CTkEntry(self.add_member_frame, placeholder_text="Postal Code")
        self.cp_entry.grid(row=11, column=0, padx=10, pady=0, sticky="ew")

        self.city_label = ctk.CTkLabel(self.add_member_frame, text="City")
        self.city_label.grid(row=12, column=0, padx=10, pady=0, sticky="w")
        self.city_entry = ctk.CTkEntry(self.add_member_frame, placeholder_text="City")
        self.city_entry.grid(row=13, column=0, padx=10, pady=(0,10), sticky="ew")

        self.subscribed_checkbox = ctk.CTkCheckBox(
            self.add_member_frame,
            text="Subscribed",
            onvalue=True,
            offvalue=False,
            variable=ctk.BooleanVar(value=False)
        )
        self.subscribed_checkbox.grid(row=14, column=0, padx=10, pady=(0, 10), sticky="w")

        self.add_button = ctk.CTkButton(self.add_member_frame, text="Add Member", command=self.adding_member)
        self.add_button.grid(row=15, column=0, padx=10, pady=(20, 10), sticky="ew")
        
        self.add_member_frame.bind("<Return>", lambda event: self.add_button.invoke())
        self.add_member_frame.bind("<Escape>", lambda event: self.add_member_frame.destroy())

    def update_member(self, member_id):
        """
        Opens a dialog to update an existing member's information.
        """
        member = self.member_service.get_member_by_id(member_id)
        if not member:
            PopUpMessage.pop_up(self, "Member not found.")
            return

        self.update_member_frame = ctk.CTkToplevel(self)
        self.update_member_frame.geometry("400x600")
        self.update_member_frame.title("UPDATE MEMBER")
        self.update_member_frame.focus_set()
        self.update_member_frame.grab_set()
        self.update_member_frame.lift()

        rows = 9
        rows_weights = [1,1,1,1,1,1,1,1,1]
        columns = 2
        columns_weights = [1,2]

        for row, w in enumerate(rows_weights):
            self.update_member_frame.grid_rowconfigure(row, weight=w)

        for column, w in enumerate(columns_weights):
            self.update_member_frame.grid_columnconfigure(column, weight=w)


        self.first_name_label = ctk.CTkLabel(
            self.update_member_frame,
            text="First Name :",
            font=ctk.CTkFont(size=13)
        )
        self.first_name_label.grid(row=0, column=0, padx=10, sticky="w")

        self.first_name_entry = ctk.CTkEntry(self.update_member_frame)
        self.first_name_entry.insert(0, member.person.first_name)
        self.first_name_entry.grid(row=0, column=1, padx=10, sticky="ew")

        self.last_name_label = ctk.CTkLabel(
            self.update_member_frame,
            text="Last Name :",
            font=ctk.CTkFont(size=13)
        )
        self.last_name_label.grid(row=1, column=0, padx=10, sticky="w")

        self.last_name_entry = ctk.CTkEntry(self.update_member_frame)
        self.last_name_entry.insert(0, member.person.last_name)
        self.last_name_entry.grid(row=1, column=1, padx=10, sticky="ew")

        self.national_number_label = ctk.CTkLabel(
            self.update_member_frame,
            text="National Number :",
            font=ctk.CTkFont(size=13)
        )
        self.national_number_label.grid(row=2, column=0, padx=10, sticky="w")

        self.national_number_entry = ctk.CTkEntry(self.update_member_frame)
        self.national_number_entry.insert(0, member.person.national_number)
        self.national_number_entry.grid(row=2, column=1, padx=10, sticky="ew")

        self.email_label = ctk.CTkLabel(
            self.update_member_frame,
            text="Email :",
            font=ctk.CTkFont(size=13)
        )
        self.email_label.grid(row=3, column=0, padx=10, sticky="w")

        self.email_entry = ctk.CTkEntry(self.update_member_frame)
        self.email_entry.insert(0, member.person.email)
        self.email_entry.grid(row=3, column=1, padx=10, sticky="ew")

        self.street_label = ctk.CTkLabel(
            self.update_member_frame,
            text="Street :",
            font=ctk.CTkFont(size=13)
                )
        self.street_label.grid(row=4, column=0, padx=10, sticky="w")

        self.street_entry = ctk.CTkEntry(self.update_member_frame)
        self.street_entry.insert(0, member.person.street)
        self.street_entry.grid(row=4, column=1, padx=10, sticky="ew")

        self.cp_label = ctk.CTkLabel(
            self.update_member_frame,
            text="Postal Code :",
            font=ctk.CTkFont(size=13)
        )
        self.cp_label.grid(row=5, column=0, padx=10, sticky="w")

        self.cp_entry = ctk.CTkEntry(self.update_member_frame)
        self.cp_entry.insert(0, member.person.cp)
        self.cp_entry.grid(row=5, column=1, padx=10, sticky="ew")

        self.city_label = ctk.CTkLabel(
            self.update_member_frame,
            text="City :",
            font=ctk.CTkFont(size=13)
        )
        self.city_label.grid(row=6, column=0, padx=10, sticky="w")

        self.city_entry = ctk.CTkEntry(self.update_member_frame)
        self.city_entry.insert(0, member.person.city)
        self.city_entry.grid(row=6, column=1, padx=10, sticky="ew")

        self.membership_entrydate_label = ctk.CTkLabel(
            self.update_member_frame,
            text="Membership Entry Date :",
            font=ctk.CTkFont(size=13)
        )
        self.membership_entrydate_label.grid(row=7, column=0, padx=10, sticky="w")

        self.membership_entrydate_entry = ctk.CTkEntry(self.update_member_frame)
        self.membership_entrydate_entry.insert(0, member.membership_entrydate)
        self.membership_entrydate_entry.grid(row=7, column=1, padx=10, sticky="ew")

        self.subscribed_checkbox = ctk.CTkCheckBox(
            self.update_member_frame,
            text="Subscribed",
            onvalue=True,
            offvalue=False,
            variable=ctk.BooleanVar(value=member.subscribed)  
        )
        self.subscribed_checkbox.grid(row=9, column=0, padx=10, sticky="ew")

        self.archived_checkbox = ctk.CTkCheckBox(
            self.update_member_frame,
            text="Archived",
            onvalue=True,
            offvalue=False,
            variable=ctk.BooleanVar(value=member.archived) 
        )
        self.archived_checkbox.grid(row=9, column=1, padx=10, pady=10, sticky="ew")

        self.update_button = ctk.CTkButton(
            self.update_member_frame, 
            text="Update Member", 
            command=lambda: self.perform_update_member(member_id)
        )
        self.update_button.grid(row=10, column=0, padx=10, pady=10, sticky="ew")
        
        self.update_member_frame.bind("<Return>", lambda event: self.update_button.invoke())
        self.update_member_frame.bind("<Escape>", lambda event: self.update_member_frame.destroy())

    def perform_update_member(self, member_id):
        """
        Performs the update of a member's information.
        """
        
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        national_number = self.national_number_entry.get()
        email = self.email_entry.get()
        street = self.street_entry.get()
        cp = self.cp_entry.get()
        city = self.city_entry.get()
        membership_entrydate = self.membership_entrydate_entry.get()
        subscribed = self.subscribed_checkbox.get()
        archived = self.archived_checkbox.get() 

        if first_name and last_name and national_number and email and street and cp and city and membership_entrydate:
            try:
                if self.member_service.update_member(
                    member_id, 
                    first_name, 
                    last_name, 
                    national_number, 
                    email, 
                    street, 
                    cp, 
                    city, 
                    membership_entrydate,
                    subscribed, 
                    archived
                ):
                    PopUpMessage.pop_up(self, "Member updated successfully.")
                    self.update_member_frame.destroy()
                    self.display_members()  
                else:
                    PopUpMessage.pop_up(self, "Error 1 updating member.")
                    self.update_member_frame.destroy()
                    self.display_members()  
            except Exception as e:
                PopUpMessage.pop_up(self, f"Error 2 updating member: {str(e)}")
        else: 
            PopUpMessage.pop_up(self, "Please fill in all fields.")

    def adding_member(self):
        
        """
        Confirms the addition of a new member and performs the addition.
        """
        id=None
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        national_number = self.national_number_entry.get()
        email = self.email_entry.get()
        street = self.street_entry.get()
        cp = self.cp_entry.get()
        city = self.city_entry.get()
        membership_entrydate = datetime.now().strftime("%Y-%m-%d") 
        archived = False 
        try:
            if not (first_name and last_name and national_number and email and street and cp and city and membership_entrydate):
                raise Exception("Please fill in all fields.")
            self.member_service.add_member(
                id=id, 
                first_name=first_name,
                last_name=last_name,
                national_number=national_number,
                email=email,
                street=street,
                cp=cp,
                city=city,
                membership_entrydate=membership_entrydate,
                archived=archived,
                subscribed=self.subscribed_checkbox.get()
            )
            PopUpMessage.pop_up(self, "Member added successfully.")
            self.add_member_frame.destroy()
            self.display_members()
        except Exception as e:
            PopUpMessage.pop_up(self, str(e))

    def delete_member(self, member_id):
        """
        Deletes a member from the JSON file and updates the display.
        """
        try:
            self.member_service.delete_member(member_id)
            self.display_members()
            PopUpMessage.pop_up(self, "Member deleted successfully.")
        except Exception as e:
            PopUpMessage.pop_up(self, str(e))

    def display_borrows_by_member(self, member_id):
        """
        Displays the borrow history of the selected member.
        """

        borrows = self.member_service.get_borrowed_books(member_id)

        for widget in self.borrows_by_member_frame.winfo_children():
            widget.destroy()

        self.borrows_by_member_frame.grid_rowconfigure(0, weight=1)
        self.borrows_by_member_frame.grid_columnconfigure(0, weight=1)
        self.borrows_by_member_frame.grid_columnconfigure(1, weight=0)


        if borrows:
            row_index = 0
            for borrow in borrows:
                book = self.member_service.get_book_by_exemplar_id(borrow.id_exemplar)
                id_label = ctk.CTkLabel(
                    self.borrows_by_member_frame,
                    text=f"ID Borrow: {borrow.id_borrow}",
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                id_label.grid(row=row_index, column=0, sticky="w", padx=15, pady=(5, 0))
                row_index += 1

                book_title_label = ctk.CTkLabel(
                    self.borrows_by_member_frame,
                    text=f"Book   : {book.title}",
                    font=ctk.CTkFont(size=16)
                )
                book_title_label.grid(row=row_index, column=0, sticky="w", padx=15, pady=(5, 0))
                row_index += 1

                Borrowed_date_label = ctk.CTkLabel(
                    self.borrows_by_member_frame,
                    text=f"Borrowed on : {borrow.borrow_date}",
                    font=ctk.CTkFont(size=16)
                )
                Borrowed_date_label.grid(row=row_index, column=0, sticky="w", padx=15, pady=(5, 0))
                row_index += 1

                exemplar_id_label = ctk.CTkLabel(
                    self.borrows_by_member_frame,
                    text=f"Exemplar ID : {borrow.id_exemplar}",
                    font=ctk.CTkFont(size=16)
                )
                exemplar_id_label.grid(row=row_index, column=0, sticky="w", padx=15, pady=(5, 0))
                row_index += 1

                book_isbn_label = ctk.CTkLabel(
                    self.borrows_by_member_frame,
                    text=f"ISBN   : {book.isbn}",
                    font=ctk.CTkFont(size=16)
                )
                book_isbn_label.grid(row=row_index, column=0, sticky="w", padx=15, pady=(5, 0))
                row_index += 1

                return_date_label = ctk.CTkLabel(
                    self.borrows_by_member_frame,
                    text=f"Return Date : {borrow.return_date}",
                    font=ctk.CTkFont(size=16)
                )
                return_date_label.grid(row=row_index, column=0, sticky="w", padx=15, pady=(5, 0))

                self.return_book_button = ctk.CTkButton(
                    self.borrows_by_member_frame,
                    text="Book Lost",
                    fg_color=Color.status_borrowed_color(),
                    hover_color=Color.secondary_color(),
                    command=lambda: self.book_lost(borrow.id_borrow, borrow.id_exemplar,borrow.member.id_member,borrow.return_date)
                )
                self.return_book_button.grid(row=row_index, column=1, padx=10, pady=10, sticky="e")

                self.return_book_button = ctk.CTkButton(
                    self.borrows_by_member_frame,
                    text="Return Book",
                    fg_color=Color.primary_color(),
                    hover_color=Color.status_available_color(),
                    command=lambda: self.return_book(borrow.id_borrow, borrow.id_exemplar,member_id,borrow.return_date),
                )
                self.return_book_button.grid(row=row_index, column=2, padx=10, pady=10, sticky="e")
                row_index += 1

                separator = ctk.CTkLabel(
                    self.borrows_by_member_frame,
                    text="" + "-" * 50,
                    font=ctk.CTkFont(size=12, weight="bold")
                )
                separator.grid(row=row_index, column=0, columnspan=3, padx=15, pady=(5, 0))
                row_index += 1
                self.borrows_by_member_frame.grid_rowconfigure(row_index, weight=1)
                self.borrows_by_member_frame.grid_columnconfigure(0, weight=1)
        else:
            no_borrows_label = ctk.CTkLabel(
                self.borrows_by_member_frame,
                text="No borrows found.",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            no_borrows_label.grid(row=0, column=0, padx=15, pady=(5, 0))

    def return_book(self, borrow_id, exemplar_id,id_member,return_date):
        """
        Handles the return of a book by updating the borrow status and exemplar availability.
        """
        due = self.payment_service.gen_price(borrow_id,False,id_member,return_date)
        PopUpMessage.pop_up(self, "Returning book with : \n - Exemplar ID: " + str(exemplar_id) + "\n - Borrow ID: " + str(borrow_id) + "\n - Price due: " + f"{due:.2f} €")
        self.display_borrows_by_member(id_member)
            
    def book_lost(self,borrow_id, exemplar_id,id_member,return_date):
        """
        Handles the case when a book is marked as lost.
        """
        due = self.payment_service.gen_price(borrow_id,True,id_member,return_date)
        PopUpMessage.pop_up(self, "Book marked as lost with \n - Exemplar ID: " + str(exemplar_id) + "\n - Price due: " + f"{due:.2f} €")
        self.display_borrows_by_member(id_member)