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
        columns = 2
        columns_weights = [1,2]

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
        self.title_label = ctk.CTkLabel(self.add_worker_frame, text="Add worker", font=("Arial", 24))
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.first_name_entry = ctk.CTkEntry(self.add_worker_frame, placeholder_text="First Name")
        self.first_name_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.last_name_entry = ctk.CTkEntry(self.add_worker_frame, placeholder_text="Last Name")
        self.last_name_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.national_number_entry = ctk.CTkEntry(self.add_worker_frame, placeholder_text="National Number")
        self.national_number_entry.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.email_entry = ctk.CTkEntry(self.add_worker_frame, placeholder_text="Email")
        self.email_entry.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.street_entry = ctk.CTkEntry(self.add_worker_frame, placeholder_text="Street")
        self.street_entry.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.cp_entry = ctk.CTkEntry(self.add_worker_frame, placeholder_text="Postal Code")
        self.cp_entry.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        self.city_entry = ctk.CTkEntry(self.add_worker_frame, placeholder_text="City")
        self.city_entry.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        self.add_button = ctk.CTkButton(self.add_worker_frame, text="Add", command=self.adding_worker)
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
                if self.worker_service.add_worker(id, first_name, last_name, national_number, email, street, cp, city):
                    PopUpMessage.pop_up(self, "Worker added successfully.")
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
                PopUpMessage.pop_up(self, f"Error adding worker: {str(e)}")
        else:
            PopUpMessage.pop_up(self, "Please fill in all fields.")

    def display_workers(self):
        """
        Displays the list of workers in the right-side frame.
        """
        # Clear the previous content in the worker list frame
        for widget in self.worker_list_frame.winfo_children():
            widget.destroy()

        self.worker_service = WorkerService()
        # Fetch all workers from the service

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

                last_name_label = ctk.CTkLabel(
                    self.worker_list_frame,
                    text=f"Last Name: {worker.person.last_name}",
                    font=ctk.CTkFont(size=16)
                )
                last_name_label.grid(row=row_index, column=0, sticky="w", padx=15)
                row_index += 1

                first_name_label = ctk.CTkLabel(
                    self.worker_list_frame,
                    text=f"First Name: {worker.person.first_name}",
                    font=ctk.CTkFont(size=16)
                )
                first_name_label.grid(row=row_index, column=0, sticky="w", padx=15)
                
                update_button = ctk.CTkButton(
                    self.worker_list_frame,
                    text="Update",
                    command=lambda w_id=worker.id_worker: self.update_worker(w_id)
                )
                update_button.grid(row=row_index-1, column=0, sticky="e", padx=10, pady=(0, 10))

                delete_button = ctk.CTkButton(
                    self.worker_list_frame,
                    text="Delete",
                    command=lambda w_id=worker.id_worker: self.delete_worker(w_id)
                )
                delete_button.grid(row=row_index, column=0, sticky="e", padx=10, pady=(0, 10))
                row_index += 1
        else:
            no_workers_label = ctk.CTkLabel(
                self.worker_list_frame,
                text="No workers found.",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            no_workers_label.grid(row=0, column=0, padx=15, pady=(5, 0))

    def delete_worker(self, worker_id):
        """
        Deletes a worker from the JSON file and updates the display.
        """
        self.worker_service.delete_worker(worker_id)
        self.display_workers()
        PopUpMessage.pop_up(self, "Worker deleted successfully.")

    def update_worker(self, worker_id):
        """
        Opens a dialog to update an existing worker's information.
        """
        worker = self.worker_service.get_worker_by_id(worker_id)
        if not worker:
            PopUpMessage.pop_up(self, "Worker not found.")
            return

        self.update_worker_frame = ctk.CTkToplevel(self)
        self.update_worker_frame.geometry("400x600")
        self.update_worker_frame.title("UPDATE WORKER")
        self.update_worker_frame.focus_set()
        self.update_worker_frame.grab_set()
        self.update_worker_frame.lift()

        rows = 9
        rows_weights = [1,1,1,1,1,1,1,1,1]
        columns = 1
        columns_weights = [1]

        for row, w in enumerate(rows_weights):
            self.update_worker_frame.grid_rowconfigure(row, weight=w)

        for column, w in enumerate(columns_weights):
            self.update_worker_frame.grid_columnconfigure(column, weight=w)

        self.first_name_entry = ctk.CTkEntry(self.update_worker_frame)
        self.first_name_entry.insert(0, worker.person.first_name)
        self.first_name_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.last_name_entry = ctk.CTkEntry(self.update_worker_frame)
        self.last_name_entry.insert(0, worker.person.last_name)
        self.last_name_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.national_number_entry = ctk.CTkEntry(self.update_worker_frame)
        self.national_number_entry.insert(0, worker.person.national_number)
        self.national_number_entry.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.email_entry = ctk.CTkEntry(self.update_worker_frame)
        self.email_entry.insert(0, worker.person.email)
        self.email_entry.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.street_entry = ctk.CTkEntry(self.update_worker_frame)
        self.street_entry.insert(0, worker.person.street)
        self.street_entry.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.cp_entry = ctk.CTkEntry(self.update_worker_frame)
        self.cp_entry.insert(0, worker.person.cp)
        self.cp_entry.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        self.city_entry = ctk.CTkEntry(self.update_worker_frame)
        self.city_entry.insert(0, worker.person.city)
        self.city_entry.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        self.update_button = ctk.CTkButton(
            self.update_worker_frame,
            text="Update Worker",
            command=lambda w_id=worker.person.id: self.perform_update_worker(w_id)
        )
        self.update_button.grid(row=10, column=0, padx=10, pady=10, sticky="ew")

    def perform_update_worker(self, worker_id):
        """
        Performs the update of a worker's information.
        """
        
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        national_number = self.national_number_entry.get()
        email = self.email_entry.get()
        street = self.street_entry.get()
        cp = self.cp_entry.get()
        city = self.city_entry.get()

        if first_name and last_name and national_number and email and street and cp and city:
            try:
                if self.worker_service.update_worker(
                    worker_id,
                    first_name,
                    last_name,
                    national_number,
                    email,
                    street,
                    cp,
                    city
                ):
                    PopUpMessage.pop_up(self, "Worker updated successfully.")
                    self.update_worker_frame.destroy()
                    self.display_workers()
                else:
                    PopUpMessage.pop_up(self, "Error 1 updating worker.")
                    self.update_worker_frame.destroy()
                    self.display_workers()
            except Exception as e:
                PopUpMessage.pop_up(self, f"Error 2 updating worker: {str(e)}")
                self.update_worker_frame.destroy()      
                self.display_workers()          
        else:
            PopUpMessage.pop_up(self, "Please fill in all fields.")
            self.update_worker_frame.destroy()
            self.display_workers()