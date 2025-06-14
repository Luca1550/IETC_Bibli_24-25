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
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface components for the WorkerPage.
        """
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.add_worker_button = ctk.CTkButton(self, text="Ajouter un travailleur", command=self.add_worker)
        self.add_worker_button.grid(row=0, column=0,sticky="w",padx=10, pady=10)
 
        self.delete_worker_button = ctk.CTkButton(self, text="Supprimer un travailleur", command=self.delete_worker)
        self.delete_worker_button.grid(row=1, column=0,sticky="w",padx=10, pady=10)

        self.display_workers_button = ctk.CTkButton(self, text="Afficher les travailleurs", command=self.display_workers)
        self.display_workers_button.grid(row=2, column=0,sticky="w",padx=10, pady=10)

    def add_worker(self):
        """
        Opens a window to add a new worker.
        """
        self.add_worker_window = ctk.CTkToplevel(self)
        self.add_worker_window.title("Ajouter un travailleur")

        self.first_name_entry = ctk.CTkEntry(self.add_worker_window, placeholder_text="Prénom")
        self.first_name_entry.pack(padx=10, pady=10)

        self.last_name_entry = ctk.CTkEntry(self.add_worker_window, placeholder_text="Nom de famille")
        self.last_name_entry.pack(padx=10, pady=10)

        self.national_number_entry = ctk.CTkEntry(self.add_worker_window, placeholder_text="Numéro national")
        self.national_number_entry.pack(padx=10, pady=10)

        self.email_entry = ctk.CTkEntry(self.add_worker_window, placeholder_text="Email")
        self.email_entry.pack(padx=10, pady=10)

        self.street_entry = ctk.CTkEntry(self.add_worker_window, placeholder_text="Rue")
        self.street_entry.pack(padx=10, pady=10)

        self.cp_entry = ctk.CTkEntry(self.add_worker_window, placeholder_text="Code postal")
        self.cp_entry.pack(padx=10, pady=10)

        self.city_entry = ctk.CTkEntry(self.add_worker_window, placeholder_text="Ville")
        self.city_entry.pack(padx=10, pady=10)

        self.add_button = ctk.CTkButton(self.add_worker_window, text="Ajouter", command=self.adding_worker)
        self.add_button.pack(padx=10, pady=10)
    
    def adding_worker(self):
        """
        Confirms the addition of a new worker and performs the addition.
        """
        id = None  # ID will be assigned by the repository
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        national_number = self.national_number_entry.get()
        email = self.email_entry.get()
        street = self.street_entry.get()
        cp = self.cp_entry.get()
        city = self.city_entry.get()

        if first_name and last_name:
            try:
                self.worker_service.add_worker(first_name, last_name, national_number, email, street, cp, city)
                PopUpMessage.pop_up("Succès", "Travailleur ajouté avec succès.")
            except Exception as e:
                PopUpMessage.pop_up("Erreur", f"Erreur lors de l'ajout du travailleur: {str(e)}")
        else:
            PopUpMessage.pop_up("Erreur", "Veuillez remplir tous les champs.")

    def delete_worker(self):
        """
        Opens a window to delete a worker.
        """
        self.delete_worker_window = ctk.CTkToplevel(self)
        self.delete_worker_window.title("Supprimer un travailleur")

        self.worker_id_entry = ctk.CTkEntry(self.delete_worker_window, placeholder_text="ID du travailleur")
        self.worker_id_entry.pack(padx=10, pady=10)

        self.delete_button = ctk.CTkButton(self.delete_worker_window, text="Supprimer", command=self.deleting_worker)
        self.delete_button.pack(padx=10, pady=10)

    def deleting_worker(self):
        """
        Confirms the deletion of a worker and performs the deletion.
        """
        worker_id = self.worker_id_entry.get()
        if worker_id:
            try:
                self.worker_service.delete_worker(worker_id)
                PopUpMessage.pop_up("Succès", "Travailleur supprimé avec succès.")
            except Exception as e:
                PopUpMessage.pop_up("Erreur", f"Erreur lors de la suppression du travailleur: {str(e)}")
        else:
            PopUpMessage.pop_up("Erreur", "Veuillez entrer un ID de travailleur valide.")


    def display_workers(self):
        """
        Displays the list of workers in a popup message.
        """
        workers = self.worker_service.get_all_workers()
        if workers:
            worker_list = "\n".join([f"{worker.id}: {worker.first_name} {worker.last_name}" for worker in workers])
            PopUpMessage.pop_up("Liste des travailleurs", worker_list)
        else:
            PopUpMessage.pop_up("Liste des travailleurs", "Aucun travailleur trouvé.")