import customtkinter as ctk
import os
from services import MemberService
from ui.components import PopUpMessage
import datetime
from datetime import datetime

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
        self.members = self.member_service.get_all_members()
        self.setup_ui()
        

    def setup_ui(self):
        """
        Sets up the UI components for the MemberPage.
        """
        ## Grid configuration for the layout
        rows = 1
        rows_weights = [1]
        columns = 2
        columns_weights = [1,5]

        for row, w in enumerate(rows_weights):
            self.grid_rowconfigure(row, weight=w)

        for column, w in enumerate(columns_weights):
            self.grid_columnconfigure(column, weight=w)

        ## UI Components

        self.member_frame = ctk.CTkFrame(self)
        self.member_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.member_frame.grid_rowconfigure(0, weight=0)
        self.member_frame.grid_rowconfigure(1, weight=1)
        self.member_frame.grid_columnconfigure(0, weight=1)
        self.member_frame.grid_columnconfigure(1, weight=0)

        ## Search bar that changes the displayed member, the bar is the same height as the button
        self.search_bar = ctk.CTkEntry(
            self.member_frame,
            placeholder_text="Search Member",
            width=200
        )
        self.search_bar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.search_bar.bind("<KeyRelease>", self.filter_members)

        self.subscribed_only_checkbox = ctk.CTkCheckBox(
            self.member_frame,
            text="Subscribed only",
            command=self.filter_members
        )
        self.subscribed_only_checkbox.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ## button that opens a dialog to add a new member
        self.add_member_button = ctk.CTkButton(
            self.member_frame,
            text="➕",
            command=self.add_member,
            width=40,
            height=40,
        )
        self.add_member_button.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

        ## Frame that contains the list of members
        self.member_list_frame = ctk.CTkScrollableFrame(
            self.member_frame
        )
        self.member_list_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.display_members()

        self.borrows_by_member_frame = ctk.CTkScrollableFrame(self)
        self.borrows_by_member_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    def filter_members(self, event=None):
        query = self.search_bar.get().lower()
        subscribed_only = self.subscribed_only_checkbox.get()  

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
                and (m.subscribed if subscribed_only else True) 
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

                delete_button = ctk.CTkButton(
                    self.member_list_frame,
                    text="Delete",
                    command=lambda m_id=member.id_member: self.delete_member(m_id)
                )
                delete_button.grid(row=row_index, column=0, sticky="w", padx=10, pady=(0, 10))

                show_borrowed_books_button = ctk.CTkButton(
                    self.member_list_frame,
                    text="Show Borrowed Books",
                    command=lambda m_id=member.id_member: self.get_selected_member_history(m_id)
                )
                show_borrowed_books_button.grid(row=row_index, column=1, sticky="w", padx=10, pady=(0, 10))
                row_index += 1

                edit_button = ctk.CTkButton(
                    self.member_list_frame,
                    text="Edit",
                    command=lambda m_id=member.id_member: self.update_member(m_id), 
                    width=80
                )
                edit_button.grid(row=row_index, column=0, sticky="w", padx=10, pady=(0, 10))
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

        rows = 9
        rows_weights = [1,1,1,1,1,1,1,1,1]
        columns = 1
        columns_weights = [1]

        for row, w in enumerate(rows_weights):
            self.add_member_frame.grid_rowconfigure(row, weight=w)

        for column, w in enumerate(columns_weights):
            self.add_member_frame.grid_columnconfigure(column, weight=w)

        self.first_name_entry = ctk.CTkEntry(self.add_member_frame, placeholder_text="First Name")
        self.first_name_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.last_name_entry = ctk.CTkEntry(self.add_member_frame, placeholder_text="Last Name")
        self.last_name_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.national_number_entry = ctk.CTkEntry(self.add_member_frame, placeholder_text="National Number")
        self.national_number_entry.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.email_entry = ctk.CTkEntry(self.add_member_frame, placeholder_text="Email")
        self.email_entry.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.street_entry = ctk.CTkEntry(self.add_member_frame, placeholder_text="Street")
        self.street_entry.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.cp_entry = ctk.CTkEntry(self.add_member_frame, placeholder_text="Postal Code")
        self.cp_entry.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        self.city_entry = ctk.CTkEntry(self.add_member_frame, placeholder_text="City")
        self.city_entry.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        self.subrscribed_checkbox = ctk.CTkCheckBox(
            self.add_member_frame,
            text="Subscribed",
            onvalue=True,
            offvalue=False,
            # Default to False
            variable=ctk.BooleanVar(value=False)  
        )
        self.subrscribed_checkbox.grid(row=8, column=0, padx=10, pady=10, sticky="ew")

        self.add_button = ctk.CTkButton(self.add_member_frame, text="Add Member", command=self.adding_member)
        self.add_button.grid(row=9, column=0, padx=10, pady=10, sticky="ew")

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
        columns = 1
        columns_weights = [1]

        for row, w in enumerate(rows_weights):
            self.update_member_frame.grid_rowconfigure(row, weight=w)

        for column, w in enumerate(columns_weights):
            self.update_member_frame.grid_columnconfigure(column, weight=w)

        self.first_name_entry = ctk.CTkEntry(self.update_member_frame)
        self.first_name_entry.insert(0, member.person.first_name)
        self.first_name_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.last_name_entry = ctk.CTkEntry(self.update_member_frame)
        self.last_name_entry.insert(0, member.person.last_name)
        self.last_name_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.national_number_entry = ctk.CTkEntry(self.update_member_frame)
        self.national_number_entry.insert(0, member.person.national_number)
        self.national_number_entry.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.email_entry = ctk.CTkEntry(self.update_member_frame)
        self.email_entry.insert(0, member.person.email)
        self.email_entry.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.street_entry = ctk.CTkEntry(self.update_member_frame)
        self.street_entry.insert(0, member.person.street)
        self.street_entry.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.cp_entry = ctk.CTkEntry(self.update_member_frame)
        self.cp_entry.insert(0, member.person.cp)
        self.cp_entry.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        self.city_entry = ctk.CTkEntry(self.update_member_frame)
        self.city_entry.insert(0, member.person.city)
        self.city_entry.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        self.membership_entrydate_entry = ctk.CTkEntry(self.update_member_frame)
        self.membership_entrydate_entry.insert(0, member.membership_entrydate)
        self.membership_entrydate_entry.grid(row=8, column=0, padx=10, pady=10, sticky="ew")

        self.subrscribed_checkbox = ctk.CTkCheckBox(
            self.update_member_frame,
            text="Subscribed",
            onvalue=True,
            offvalue=False,
            variable=ctk.BooleanVar(value=member.subscribed)  # Set to current subscription status
        )
        self.subrscribed_checkbox.grid(row=9, column=0, padx=10, pady=10, sticky="ew")

        self.archived_checkbox = ctk.CTkCheckBox(
            self.update_member_frame,
            text="Archived",
            onvalue=True,
            offvalue=False,
            variable=ctk.BooleanVar(value=member.archived)  # Set to current archived status
        )
        self.archived_checkbox.grid(row=9, column=1, padx=10, pady=10, sticky="ew")

        self.update_button = ctk.CTkButton(
            self.update_member_frame, 
            text="Update Member", 
            command=lambda: self.perform_update_member(member_id)
        )
        self.update_button.grid(row=10, column=0, padx=10, pady=10, sticky="ew")

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
        subscribed = self.subrscribed_checkbox.get()
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
                self.update_member_frame.destroy()
                self.display_members()

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
        membership_entrydate = datetime.now().strftime("%Y-%m-%d")  # Today's date
        archived = False  # Default value for archived status

        member_added = self.member_service.add_member(
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
            subscribed=self.subrscribed_checkbox.get()
        )

        if member_added:
            PopUpMessage.pop_up(self, "Member added successfully.")
            self.add_member_frame.destroy()
            self.display_members()
        else:
            PopUpMessage.pop_up(self, "Error adding member.")
            self.add_member_frame.destroy()
            self.display_members()

    def delete_member(self, member_id):
        """
        Deletes a member from the JSON file and updates the display.
        """
        self.member_service.delete_member(member_id)
        self.display_members()
        PopUpMessage.pop_up(self, "Member deleted successfully.")

    def get_selected_member_history(self, member_id):
        """
        Handles the selection of a member from the list.
        """
        PopUpMessage.pop_up(self, f"Selected Member ID: {member_id}")

        self.display_borrows_by_member()

    def display_borrows_by_member(self):
        """
        Displays the borrow history of the selected member.
        """
        for widget in self.borrows_by_member_frame.winfo_children():
            widget.destroy()

        self.borrows_by_member_frame.grid_rowconfigure(0, weight=1)
        self.borrows_by_member_frame.grid_columnconfigure(0, weight=1)
        self.borrows_by_member_frame.grid_columnconfigure(1, weight=0)

        self.borrows_by_member_label = ctk.CTkLabel(
            self.borrows_by_member_frame,
            text="Borrowed book",
        )

        self.borrows_by_member_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.return_book_button = ctk.CTkButton(
            self.borrows_by_member_frame,
            text="Return Book",
            command=lambda: PopUpMessage.pop_up(self, "Return Book functionality not implemented yet.")
        )
        self.return_book_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")



