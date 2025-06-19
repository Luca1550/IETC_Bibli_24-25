import customtkinter as ctk
import os
from services import MemberService
from ui.components import PopUpMessage

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
        columns = 1
        columns_weights = [1]

        for row, w in enumerate(rows_weights):
            self.grid_rowconfigure(row, weight=w)

        for column, w in enumerate(columns_weights):
            self.grid_columnconfigure(column, weight=w)

        ## UI Components

        self.manage_member_frame = ctk.CTkFrame(self)
        self.manage_member_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.add_member_button = ctk.CTkButton(
            self.manage_member_frame,
            text="Ajouter Membre",
            command=self.add_member
        )
        self.add_member_button.grid(row=0, column=0, padx=10, pady=10)

        self.member_list_frame = ctk.CTkFrame(self.manage_member_frame)
        self.member_list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")



    def display_members(self):
        """
        Displays the list of members in the right-side frame.
        """
        self.member_service = MemberService()
        # Fetch all members from the service

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
                    text=f"Nom: {member.person.last_name}",
                    font=ctk.CTkFont(size=16)
                )
                last_name_label.grid(row=row_index, column=0, sticky="w", padx=15)
                row_index += 1

                first_name_label = ctk.CTkLabel(
                    self.member_list_frame,
                    text=f"Prénom: {member.person.first_name}",
                    font=ctk.CTkFont(size=16)
                )
                first_name_label.grid(row=row_index, column=0, sticky="w", padx=15)
                row_index += 1

                delete_button = ctk.CTkButton(
                    self.member_list_frame,
                    text="Supprimer",
                    command=lambda m_id=member.id_member: self.delete_member(m_id)
                )
                delete_button.grid(row=row_index, column=0, sticky="e", padx=10, pady=(0, 10))
                row_index += 1
        else:
            no_members_label = ctk.CTkLabel(
                self.member_list_frame,
                text="Aucun membre trouvé.",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            no_members_label.grid(row=0, column=0, padx=15, pady=(5, 0))

    def add_member(self):
        """
        Opens a dialog to add a new member and updates the display.
        """

    def delete_member(self, member_id):
        """
        Deletes a member from the JSON file and updates the display.
        """
        self.member_service.delete_member(member_id)
        self.display_members()
        PopUpMessage.pop_up(self, "Membre supprimé avec succès.")

    def get_selected_member_history(self, member_id):
        """
        Handles the selection of a member from the list.
        """
        PopUpMessage.pop_up(self, f"Selected Member ID: {member_id}")
