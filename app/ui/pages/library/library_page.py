
import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from services import LibraryService


class LibraryPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.library_service = LibraryService()

        self.selected_library = None
        self.libraries = []
        self.setup_ui()
        self.load_libraries()

    def setup_ui(self):
        #ici je tape 0 pour dire que ca prend toute la fenetre et 1 pour qu'elle s'adapte 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  

        # le truc sticky nsew est globalement pour dire que la page s'etire dans toutes la grille du nord ouest,.... 
        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.form_title = ctk.CTkLabel(self.main_panel, text="Bibliothèque", font=ctk.CTkFont(size=18, weight="bold"))
        self.form_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        self.paramlib = self.library_service.get_library_parameters()
        if self.paramlib:
            #faut que je rajoute le truc pour dire que si self.paramlib[1] exist c'est l'explosion 
            lib_params=self.paramlib[0]
            #ici j'utilise enumerate parce que ca me permet d'avoir un genre d'index avec i et puis le nom et la valeur
            
            for i,(key, value) in enumerate(lib_params.items(),start=1):
                if key != "id" :
                    #capitalize c'est pour mettre une maj au debut du mot en gros du gros et le reste en minuscule
                    label_txt= key.replace("_"," ").capitalize()
                
                    self.label= ctk.CTkLabel(self.main_panel,text=label_txt)
                    self.label.grid(row=i, column=0, sticky="w", padx=1, pady=1)

                    self.label_entry = ctk.CTkEntry(self.main_panel)
                    self.label_entry.grid(row=i, column=1, sticky="ew", pady=1)
                    row_index = i

        self.save_button = ctk.CTkButton(self.main_panel, text="Save", command=self.library_service.update_library)
        self.save_button.grid(row=row_index+1, column=0, columnspan=2, pady=10)

        self.main_panel.grid_columnconfigure(1, weight=1)  # La colonne 1 (les champs) s'étend

    def load_libraries(self):
        self.libraries = self.library_service.get_library_parameters()

        if self.libraries:
            self.selected_library = self.libraries[0]
            self.populate_form(self.selected_library)
            #self.set_form_state(True)
            name = self.selected_library.get("name")
            self.form_title.configure(text=name)
        else:
            # Si aucune bibliothèque : on prépare un formulaire vide
            self.selected_library = None
            #self.set_form_state(True)
            self.form_title.configure(text="Nouvelle bibliothèque")

    def populate_form(self, library: dict):
        """
        Remplit tous les champs dynamiques du formulaire avec les valeurs de la bibliothèque passée.
        """
        


    """ def set_form_state(self, state: bool):
        
        for entry in self.entries.values():
            entry.configure(state="normal" if state else "disabled")
        self.save_button.configure(state="normal" if state else "disabled")"""

    """def save_library(self):
        new_data = {}
        for key, entry in self.entries.items():
            value = entry.get()
            # Essayer de convertir les types selon le champ attendu (float, int, etc.)
            try:
                if "price" in key or "fine" in key or "amount" in key:
                    new_data[key] = float(value)
                elif "limit" in key or "delay" in key or "id" in key:
                    new_data[key] = int(value)
                else:
                    new_data[key] = value
            except ValueError:
                new_data[key] = value  # Garde en texte si erreur de conversion

        self.library_service.save_library(new_data)

        name = new_data.get("name", "Bibliothèque")
        self.form_title.configure(text=name)"""

