import customtkinter as ctk
import os
from services import WorkerService
from ui.components import PopUpMessage

class WorkerPage(ctk.CTkFrame):
    """
    WorkerPage class that manages the worker management interface.
    It allows adding, deleting, and displaying workers.
    """
    def __init__(self, parent, **kwargs):
        """
        Initializes the WorkerPage class and sets up the UI components.
        """
        super().__init__(parent, **kwargs)
        self.worker_service = WorkerService()
        self.workers = self.worker_service.get_all_workers()
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface components for the WorkerPage.
        """

        ## Grid configuration for the layout
        rows = 9
        rows_weights = [1,1,1,1,1,1,1,1,1]
        columns = 9
        columns_weights = [1,2,1,1,1,1,1,1,1]

        for row, w in enumerate(rows_weights):
            self.grid_rowconfigure(row, weight=w)

        for column, w in enumerate(columns_weights):
            self.grid_columnconfigure(column, weight=w)

        ## UI Components

        self.add_worker_frame = ctk.CTkFrame(self)
        self.add_worker_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Make column 0 expandable (to center content)
        self.add_worker_frame.grid_columnconfigure(0, weight=1)

        # Widgets
        self.title_label = ctk.CTkLabel(self.add_worker_frame, text="Ajout employé", font=("Arial", 24))
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.first_name_entry = ctk.CTkEntry(self.add_worker_frame, placeholder_text="Prénom")
        self.first_name_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.last_name_entry = ctk.CTkEntry(self.add_worker_frame, placeholder_text="Nom de famille")
        self.last_name_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.national_number_entry = ctk.CTkEntry(self.add_worker_frame, placeholder_text="Numéro national")
        self.national_number_entry.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.email_entry = ctk.CTkEntry(self.add_worker_frame, placeholder_text="Email")
        self.email_entry.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.street_entry = ctk.CTkEntry(self.add_worker_frame, placeholder_text="Rue")
        self.street_entry.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.cp_entry = ctk.CTkEntry(self.add_worker_frame, placeholder_text="Code postal")
        self.cp_entry.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        self.city_entry = ctk.CTkEntry(self.add_worker_frame, placeholder_text="Ville")
        self.city_entry.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        self.add_button = ctk.CTkButton(self.add_worker_frame, text="Ajouter", command=self.adding_worker)
        self.add_button.grid(row=8, column=0, padx=10, pady=10, sticky="ew")

        self.worker_list_frame = ctk.CTkFrame(self)
        self.worker_list_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.worker_list_frame.grid_columnconfigure(0, weight=1)

        self.display_workers()

    def adding_worker(self):
        """
        Confirms the addition of a new worker and performs the addition.
        """
        id = None  
        # ID will be assigned by the repository
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        national_number = self.national_number_entry.get()
        email = self.email_entry.get()
        street = self.street_entry.get()
        cp = self.cp_entry.get()
        city = self.city_entry.get()

        if first_name and last_name and national_number and email and street and cp and city:
            try:
                self.worker_service.add_worker(id, first_name, last_name, national_number, email, street, cp, city)
                PopUpMessage.pop_up(self, "Travailleur ajouté avec succès.")
                self.display_workers()
                # Clear the input fields after adding
                self.first_name_entry.delete(0, 'end')
                self.last_name_entry.delete(0, 'end')
                self.national_number_entry.delete(0, 'end')
                self.email_entry.delete(0, 'end')
                self.street_entry.delete(0, 'end')
                self.cp_entry.delete(0, 'end')
                self.city_entry.delete(0, 'end')
            except Exception as e:
                PopUpMessage.pop_up(self, f"Erreur lors de l'ajout du travailleur: {str(e)}")
        else:
            PopUpMessage.pop_up(self, "Veuillez remplir tous les champs.")

    def display_workers(self):
        """
        Displays the list of workers in the right-side frame.
        """
        # Clear previous widgets
        for widget in self.worker_list_frame.winfo_children():
            widget.destroy()

        workers = self.worker_service.get_all_workers()
        if workers:
            row_index = 0
            for worker in workers:
                id_label = ctk.CTkLabel(
                    self.worker_list_frame,
                    text=f"ID: {worker.id_worker}",
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                id_label.grid(row=row_index, column=0, sticky="w", padx=15, pady=(5, 0))
                row_index += 1

                name_label = ctk.CTkLabel(
                    self.worker_list_frame,
                    text=f"Nom: {worker.person.last_name}, Prénom: {worker.person.first_name}",
                    font=ctk.CTkFont(size=16)
                )
                name_label.grid(row=row_index, column=0, sticky="w", padx=15, pady=(0, 5))
                row_index += 1

                delete_button = ctk.CTkButton(
                    self.worker_list_frame,
                    text="Supprimer",
                    command=lambda w_id=worker.id_worker: self.delete_worker(w_id)
                )
                delete_button.grid(row=row_index, column=0, sticky="e", padx=10, pady=(0, 10))
                row_index += 1
        else:
            no_workers_label = ctk.CTkLabel(
                self.worker_list_frame,
                text="Aucun travailleur trouvé.",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            no_workers_label.grid(row=0, column=0, padx=15, pady=(5, 0))


    def delete_worker(self, worker_id):
        """
        Deletes a worker from the JSON file and updates the display.
        """
        self.worker_service.delete_worker(worker_id)
        self.display_workers()
        PopUpMessage.pop_up(self, "Travailleur supprimé avec succès.")
        self.first_name_entry.delete(0, 'end')
        self.last_name_entry.delete(0, 'end')
        self.national_number_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.street_entry.delete(0, 'end')
        self.cp_entry.delete(0, 'end')
        self.city_entry.delete(0, 'end')