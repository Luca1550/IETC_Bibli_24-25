
import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from services import ReservationService
from ui.components import PopUpMessage

#ok donc a gauche on va pouvoir voir les reservations et qu'elles soient clickable 
#a droite on peut faire une reservation et quand on clique sur une reservation on a le bouton update a la place de add 



class ReservationPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.reservation_service = ReservationService()
        self.setup_ui()
        
    def setup_ui(self):
        

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  

        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        

        self.form_title = ctk.CTkLabel(self.main_panel, text="Rerservation", font=ctk.CTkFont(size=18, weight="bold"))
        self.form_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self.paramres = self.reservation_service.get_all()

        
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

        self.left_label = ctk.CTkLabel(self.left_panel, text="Mes Réservations", font=ctk.CTkFont(size=16, weight="bold"))
        self.left_label.pack(pady=(10, 5))

        self.reservation_listbox = ctk.CTkTextbox(self.left_panel, width=200, height=400)
        self.reservation_listbox.pack(expand=True, fill="both", padx=10, pady=10)

        self.paramres = self.reservation_service.get_all()
        for res in self.paramres:
            self.reservation_listbox.insert("end", f"{res.nom} - {res.date}\n")

        self.right_panel = ctk.CTkFrame(self.main_panel)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        self.form_title = ctk.CTkLabel(self.right_panel, text="Nouvelle Réservation", font=ctk.CTkFont(size=18, weight="bold"))
        self.form_title.pack(pady=(10, 10))

        self.name_entry = ctk.CTkEntry(self.right_panel, placeholder_text="Nom")
        self.name_entry.pack(pady=5, padx=20, fill="x")

        self.date_entry = ctk.CTkEntry(self.right_panel, placeholder_text="Date (YYYY-MM-DD)")
        self.date_entry.pack(pady=5, padx=20, fill="x")

        self.submit_button = ctk.CTkButton(self.right_panel, text="Réserver")
        self.submit_button.pack(pady=20)

