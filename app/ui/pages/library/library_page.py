
import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from services import LibraryService
from ui.components import PopUpMessage

class LibraryPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.library_service = LibraryService()
        self.libraries = []
        self.setup_ui()
        

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

        if len(self.paramlib) ==1:
            self.lib_form()
        else:
            PopUpMessage.pop_up(self, "error: You cannot have less or more than one library")
        self.main_panel.grid_columnconfigure(1, weight=1)  # La colonne 1 (les champs) s'étend


    def lib_form(self):
        if self.paramlib:
            #faut que je rajoute le truc pour dire que si self.paramlib[1] exist c'est l'explosion 
            lib_params=self.paramlib[0]
            #ici j'utilise enumerate parce que ca me permet d'avoir un genre d'index avec i et puis le nom et la valeur
            self.entries={}
            for i,(key, value) in enumerate(lib_params.items(),start=1):
                if key != "id" :
                    #capitalize c'est pour mettre une maj au debut du mot en gros du gros et le reste en minuscule
                    #il faut que je stock jsp ou ce que j'ai rentré comme info
                    label_txt= key.replace("_"," ").capitalize()
                
                    self.label= ctk.CTkLabel(self.main_panel,text=label_txt)
                    self.label.grid(row=i, column=0, sticky="w", padx=1, pady=1)

                    self.label_entry = ctk.CTkEntry(self.main_panel)
                    self.label_entry.grid(row=i, column=1, sticky="ew", pady=1)
                    self.label_entry.insert(0, str(value))
                    self.entries[key] = self.label_entry
                    row_index = i

        self.save_button = ctk.CTkButton(self.main_panel, text="Save", command=self.save_libraries)
        self.save_button.grid(row=row_index+1, column=0, columnspan=2, pady=10)
    def save_libraries(self):
        updated_param={}
        updated_param["id"] =self.paramlib[0]["id"]
        for key, value in self.entries.items():
            updated_param[key] = value.get()
            print(value.get())
        self.library_service.update_library(**updated_param)
    #def add_buton(self):