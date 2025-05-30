
import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from services import LibraryService


class LibraryPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.library_service = LibraryService()
        self.libraries = []
        self.selected_library = None
        
        self.setup_ui()
        self.load_libraries()
    
    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.left_panel = ctk.CTkFrame(self)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        self.left_panel.grid_rowconfigure(1, weight=1)
        
        self.left_title = ctk.CTkLabel(self.left_panel, text="Bibliothèques", font=("Arial", 16, "bold"))
        self.left_title.grid(row=0, column=0, pady=(10, 5), padx=10)
        
        self.libraries_listbox = tk.Listbox(self.left_panel, selectmode=tk.SINGLE, font=("Arial", 10))
        self.libraries_listbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.libraries_listbox.bind("<<ListboxSelect>>", self.on_library_select)
        
        self.left_buttons_frame = ctk.CTkFrame(self.left_panel)
        self.left_buttons_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        self.new_button = ctk.CTkButton(self.left_buttons_frame, text="Nouvelle", command=self.new_library)
        self.new_button.pack(pady=5, fill="x")
        
        self.refresh_button = ctk.CTkButton(self.left_buttons_frame, text="Actualiser", command=self.load_libraries)
        self.refresh_button.pack(pady=5, fill="x")
        
        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        
        self.form_title = ctk.CTkLabel(self.right_panel, text="Paramètres de la bibliothèque", font=("Arial", 16, "bold"))
        self.form_title.grid(row=0, column=0, columnspan=2, pady=(10, 20), padx=20)
        
        self.create_form()
    
    def create_form(self):
        row = 1
        
        labels = [
            ("Nom:", "name"),
            ("Amende par jour (€):", "fine_per_day"),
            ("Montant d'abonnement (€):", "subscribe_amount"),
            ("Limite d'emprunt:", "limit_borrow"),
            ("Prix emprunt avec abonnement (€):", "borrow_price_with_sub"),
            ("Prix emprunt sans abonnement (€):", "borrow_price_without_sub"),
            ("Délai d'emprunt (jours):", "borrow_delay"),
            ("URL du logo:", "url_logo"),
        ]
        
        self.form_entries = {}  # stocke les widgets avec leur clé
        
        for label_text, key in labels:
            ctk.CTkLabel(self.right_panel, text=label_text).grid(row=row, column=0, sticky="w", padx=20, pady=5)
            entry = ctk.CTkEntry(self.right_panel, width=300)
            entry.grid(row=row, column=1, sticky="w", padx=20, pady=5)
            self.form_entries[key] = entry
            row += 1
        
        self.buttons_frame = ctk.CTkFrame(self.right_panel)
        self.buttons_frame.grid(row=row, column=0, columnspan=2, pady=20, padx=20, sticky="ew")
        
        self.save_button = ctk.CTkButton(self.buttons_frame, text="Sauvegarder", command=self.save_library, fg_color="green")
        self.save_button.pack(side="left", padx=5)
        
        self.cancel_button = ctk.CTkButton(self.buttons_frame, text="Annuler", command=self.clear_form, fg_color="gray")
        self.cancel_button.pack(side="left", padx=5)
        
        self.set_form_state(False)
    
    def load_libraries(self):
        try:
            self.libraries = self.library_service.get_library_parameters()
            self.libraries_listbox.delete(0, tk.END)
            
            for library in self.libraries:
                try:
                    name = getattr(library, "name", None) if not isinstance(library, dict) else library.get("name")
                    if name:
                        self.libraries_listbox.insert(tk.END, name)
                    else:
                        fallback = getattr(library, "id", "inconnu") if not isinstance(library, dict) else library.get("id", "inconnu")
                        self.libraries_listbox.insert(tk.END, f"Bibliothèque {fallback}")
                except Exception as e:
                    print(f"Erreur ajout bibliothèque: {e}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Chargement échoué : {str(e)}")
    
    def on_library_select(self, event):
        selection = self.libraries_listbox.curselection()
        if selection:
            index = selection[0]
            self.selected_library = self.libraries[index]
            self.populate_form(self.selected_library)
            self.set_form_state(True)
    
    def populate_form(self, library):
        self.clear_form()
        
        for key, entry in self.form_entries.items():
            value = getattr(library, key, None) if not isinstance(library, dict) else library.get(key)
            if value is not None:
                entry.insert(0, str(value))
    
    def clear_form(self):
        for entry in self.form_entries.values():
            entry.delete(0, tk.END)
        self.selected_library = None
        self.libraries_listbox.selection_clear(0, tk.END)
    
    def set_form_state(self, enabled):
        state = "normal" if enabled else "disabled"
        for entry in self.form_entries.values():
            entry.configure(state=state)
        self.save_button.configure(state=state)
        self.cancel_button.configure(state=state)
    
    def new_library(self):
        self.clear_form()
        self.set_form_state(True)
        self.form_title.configure(text="Nouvelle bibliothèque")
    
    def save_library(self):
        try:
            values = {key: entry.get().strip() for key, entry in self.form_entries.items()}
            
            # Validations et conversions
            if not values["name"]:
                messagebox.showerror("Erreur", "Le nom est obligatoire.")
                return
            
            float_keys = ["fine_per_day", "subscribe_amount", "borrow_price_with_sub", "borrow_price_without_sub"]
            int_keys = ["limit_borrow", "borrow_delay"]
            
            for key in float_keys:
                values[key] = float(values[key])
            for key in int_keys:
                values[key] = int(values[key])
            
            if self.selected_library is None:
                result = self.library_service.add_library(**values)
                if isinstance(result, str) and result.startswith("🛑"):
                    messagebox.showerror("Erreur", result)
                    return
                messagebox.showinfo("Succès", "Bibliothèque créée avec succès!")
            else:
                result = self.library_service.update_library(
                    id=getattr(self.selected_library, "id", self.selected_library.get("id")),
                    **values
                )
                if isinstance(result, str) and result.startswith("🛑"):
                    messagebox.showerror("Erreur", result)
                    return
                elif result:
                    messagebox.showinfo("Succès", "Mise à jour réussie!")
                else:
                    messagebox.showerror("Erreur", "Échec de la mise à jour.")
                    return
            
            self.load_libraries()
            self.clear_form()
            self.set_form_state(False)
            self.form_title.configure(text="Paramètres de la bibliothèque")
        
        except ValueError as e:
            messagebox.showerror("Erreur", f"Valeur incorrecte: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {str(e)}")


def page_config(parent):
    return LibraryPage(parent)
