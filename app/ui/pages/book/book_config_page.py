import customtkinter as ctk
from services import AuthorService,ThemeService,EditorService,CollectionService
from ui.components import PopUpMessage

class BookConfigPage(ctk.CTkToplevel):
    """Page for managing book configurations such as authors, themes, editors, and collections."""
    def __init__(self, theme_service : ThemeService):
        """Initialize the book configuration page."""
        super().__init__()
        self.theme_service = theme_service
        
        btn_add_theme = ctk.CTkButton(self, width=150, text="➕ Add Themes", command=self.open_add_theme_page)
        btn_add_theme.pack(pady=10)

        btn_delete_theme = ctk.CTkButton(self, width=150, text="🗑️ Delete Themes", command=self.open_delete_theme_page)
        btn_delete_theme.pack(pady=10)
        
        ctk.CTkButton(self,width=100,text="➕ Add Themes", command=self.open_add_theme_page)
        ctk.CTkButton(self,width=100,text="🗑️ Delete Themes", command=self.open_delete_theme_page)
    
    def open_delete_theme_page(self):
        """Open the page to delete themes."""
        delete_theme_page = DeleteThemePage(self.theme_service)
        self.wait_window(delete_theme_page)
    
    def open_add_theme_page(self):
        """Open the page to add a new theme."""
        add_theme_page = AddThemePage(self.theme_service)
        self.wait_window(add_theme_page)

class AddThemePage(ctk.CTkToplevel):
    """Page for adding a new theme."""
    def __init__(self, theme_service : ThemeService):
        super().__init__()
        self.theme_service = theme_service
        
        self.title = "Add Theme"
        
        ctk.CTkLabel(self, text="Name", anchor="w").pack(fill="x", padx=20)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(fill="x", padx=20)
        
        ctk.CTkButton(self, text="✅ Add Theme", command=self.confirm_action).pack(pady=10)
        ctk.CTkButton(self, text="❌ Cancel", fg_color="transparent", command=self.destroy).pack()
        
    def confirm_action(self):
        """Confirm the action of adding a new theme."""
        try:
            self.theme_service.add_theme(
                name=self.name_entry.get(),
            )

            PopUpMessage.pop_up(self, "Theme added ✅")
            self.destroy()

        except Exception as e:
            PopUpMessage.pop_up(self, str(e).lower())

class DeleteThemePage(ctk.CTkToplevel):
    def __init__(self, theme_service: ThemeService):
        super().__init__()
        self.theme_service = theme_service
        self.themes = []

        self.title("Delete Themes")
        self.geometry("500x600")

        title_label = ctk.CTkLabel(self, text="🗑️ Delete Themes", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(10, 5))

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=480, height=500)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_themes()

    def load_themes(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            self.themes = self.theme_service.get_all()

            if not self.themes:
                empty_label = ctk.CTkLabel(self.scroll_frame, text="No themes available.", text_color="gray")
                empty_label.pack(pady=20)
                return

            for theme in self.themes:
                frame = ctk.CTkFrame(self.scroll_frame)
                frame.pack(fill="x", pady=5, padx=10)

                name_label = ctk.CTkLabel(frame, text=f"🏷️ {theme.name}", anchor="w")
                name_label.pack(side="left", padx=10, pady=5, fill="x", expand=True)

                delete_btn = ctk.CTkButton(
                    frame,
                    text="🗑️ Supprimer",
                    fg_color="red",
                    hover_color="#cc0000",
                    width=100,
                    command=lambda t=theme: self.confirm_delete(t)
                )
                delete_btn.pack(side="right", padx=10)

        except Exception as e:
            PopUpMessage.pop_up(self, f"Erreur de chargement : {str(e)}")

    def confirm_delete(self, theme):
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Confirmer la suppression")
        confirm_window.geometry("300x150")
        confirm_window.grab_set()

        ctk.CTkLabel(
            confirm_window,
            text=f"Supprimer le thème :\n'{theme.name}' ?",
            wraplength=250
        ).pack(pady=20)

        btn_frame = ctk.CTkFrame(confirm_window, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Oui",
            fg_color="red",
            hover_color="#cc0000",
            command=lambda: [
                self.theme_service.delete_theme(name=theme.name),
                confirm_window.destroy()
            ]
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Non",
            command=confirm_window.destroy
        ).pack(side="right", padx=10)

    def delete_theme(self, theme):
        try:
            self.theme_service.delete_theme(theme.id)
            PopUpMessage.pop_up(self, f"✅ Thème supprimé")
            self.load_themes()
        except Exception as e:
            PopUpMessage.pop_up(self, f"Erreur : {str(e)}")


class AddEditorPage(ctk.CTkToplevel):
    def __init__(self, editor_service : EditorService):
        super().__init__()
        self.editor_service = editor_service
        
        self.title = "Add Editor"
        
        ctk.CTkLabel(self, text="Name", anchor="w").pack(fill="x", padx=20)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(fill="x", padx=20)
        
        ctk.CTkButton(self, text="✅ Add Editor", command=self.confirm_action).pack(pady=10)
        ctk.CTkButton(self, text="❌ Cancel", fg_color="transparent", command=self.destroy).pack()
        
    def confirm_action(self):
        try:
            self.editor_service.add_editor(
                name=self.name_entry.get(),
            )

            PopUpMessage.pop_up(self, "Editor added ✅")
            self.destroy()

        except Exception as e:
            PopUpMessage.pop_up(self, str(e).lower())

class AddCollectionPage(ctk.CTkToplevel):
    def __init__(self, collection_service : CollectionService):
        super().__init__()
        self.collection_service = collection_service
        
        self.title = "Add Collection"
        
        ctk.CTkLabel(self, text="Name", anchor="w").pack(fill="x", padx=20)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(fill="x", padx=20)
        
        ctk.CTkButton(self, text="✅ Add Collection", command=self.confirm_action).pack(pady=10)
        ctk.CTkButton(self, text="❌ Cancel", fg_color="transparent", command=self.destroy).pack()
        
    def confirm_action(self):
        try:
            self.collection_service.add_collection(
                name=self.name_entry.get(),
            )

            PopUpMessage.pop_up(self, "Collection added ✅")
            self.destroy()

        except Exception as e:
            PopUpMessage.pop_up(self, str(e).lower())

class AddAuthorPage(ctk.CTkToplevel):
    def __init__(self, author_service : AuthorService):
        super().__init__()
        self.author_service = author_service
        
        self.title = "Add Author"
        
        ctk.CTkLabel(self, text="first name", anchor="w").pack(fill="x", padx=20)
        self.first_name_entry = ctk.CTkEntry(self)
        self.first_name_entry.pack(fill="x", padx=20)
        
        ctk.CTkLabel(self, text="Last name", anchor="w").pack(fill="x", padx=20)
        self.last_name_entry = ctk.CTkEntry(self)
        self.last_name_entry.pack(fill="x", padx=20)
        
        ctk.CTkLabel(self, text="National number", anchor="w").pack(fill="x", padx=20)
        self.national_number_entry = ctk.CTkEntry(self)
        self.national_number_entry.pack(fill="x", padx=20)
        
        ctk.CTkLabel(self, text="Email", anchor="w").pack(fill="x", padx=20)
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack(fill="x", padx=20)
        
        ctk.CTkLabel(self, text="Street", anchor="w").pack(fill="x", padx=20)
        self.street_entry = ctk.CTkEntry(self)
        self.street_entry.pack(fill="x", padx=20)
        
        ctk.CTkLabel(self, text="CP", anchor="w").pack(fill="x", padx=20)
        self.cp_entry = ctk.CTkEntry(self)
        self.cp_entry.pack(fill="x", padx=20)
        
        ctk.CTkLabel(self, text="City", anchor="w").pack(fill="x", padx=20)
        self.city_entry = ctk.CTkEntry(self)
        self.city_entry.pack(fill="x", padx=20)
        
        ctk.CTkButton(self, text="✅ Add Author", command=self.confirm_action).pack(pady=10)
        ctk.CTkButton(self, text="❌ Cancel", fg_color="transparent", command=self.destroy).pack()
        
    def confirm_action(self):
        try:
            self.author_service.add_author(
                first_name=self.first_name_entry.get(),
                last_name=self.last_name_entry.get(),
                national_number=self.national_number_entry.get(),
                email=self.email_entry.get(),
                street=self.street_entry.get(),
                cp=self.cp_entry.get(),
                city=self.city_entry.get()
            )

            PopUpMessage.pop_up(self, "Author added ✅")
            self.destroy()

        except Exception as e:
            PopUpMessage.pop_up(self, str(e).lower())