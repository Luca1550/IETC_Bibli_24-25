import customtkinter as ctk
from services import AuthorService,ThemeService,EditorService,CollectionService
from ui.components import PopUpMessage

class BookConfigPage(ctk.CTkToplevel):
    """Page for managing book configurations such as authors, themes, editors, and collections."""
    def __init__(self, theme_service : ThemeService, editor_service : EditorService, collection_service : CollectionService, author_service : AuthorService):
        """Initialize the book configuration page."""
        super().__init__()

        self.focus_set()
        self.grab_set()
        self.lift()
        self.title("Configurations")
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.theme_service = theme_service
        self.editor_service = editor_service
        self.collection_service = collection_service
        self.author_service = author_service
        
        ctk.CTkLabel(self, text="Themes", font=("Roboto", 16, "bold")).grid(row=0, column=0, pady=(10, 0))
        ctk.CTkLabel(self, text="Editors", font=("Roboto", 16, "bold")).grid(row=0, column=1, pady=(10, 0))
        ctk.CTkLabel(self, text="Collections", font=("Roboto", 16, "bold")).grid(row=0, column=2, pady=(10, 0))
        ctk.CTkLabel(self, text="Authors", font=("Roboto", 16, "bold")).grid(row=0, column=3, pady=(10, 0))

        ctk.CTkButton(self, width=150, text="➕ Add Themes", command=self.open_add_theme_page).grid(row=1, column=0, pady=5, padx=10)
        ctk.CTkButton(self, width=150, text="🗑️ Delete Themes", command=self.open_delete_theme_page).grid(row=2, column=0, pady=(5,20), padx=10)

        ctk.CTkButton(self, width=150, text="➕ Add Editors", command=self.open_add_editor_page).grid(row=1, column=1, pady=5, padx=10)
        ctk.CTkButton(self, width=150, text="🗑️ Delete Editors", command=self.open_delete_editor_page).grid(row=2, column=1, pady=(5,20), padx=10)

        ctk.CTkButton(self, width=150, text="➕ Add Collections", command=self.open_add_collection_page).grid(row=1, column=2, pady=5, padx=10)
        ctk.CTkButton(self, width=150, text="🗑️ Delete Collections", command=self.open_delete_collection_page).grid(row=2, column=2, pady=(5,20), padx=10)

        ctk.CTkButton(self, width=150, text="➕ Add Authors", command=self.open_add_author_page).grid(row=1, column=3, pady=5, padx=10)
        ctk.CTkButton(self, width=150, text="🗑️ Delete Authors", command=self.open_delete_author_page).grid(row=2, column=3, pady=(5,20), padx=10)
        
        
        self.bind("<Escape>", lambda event: self.destroy())
    
    def open_add_theme_page(self):
        """Open the page to add a new theme."""
        add_theme_page = AddThemePage(self.theme_service)
        self.wait_window(add_theme_page)
    
    def open_delete_theme_page(self):
        """Open the page to delete themes."""
        delete_theme_page = DeleteThemePage()
        self.wait_window(delete_theme_page)
    
    
    def open_add_editor_page(self):
        """Open the page to add a new editor."""
        add_editor_page = AddEditorPage(self.editor_service)
        self.wait_window(add_editor_page)
    
    def open_delete_editor_page(self):
        """Open the page to delete editors."""
        delete_editor_page = DeleteEditorPage()
        self.wait_window(delete_editor_page)
    
    
    def open_add_collection_page(self):
        """Open the page to add a new collection."""
        add_collection_page = AddCollectionPage(self.collection_service)
        self.wait_window(add_collection_page)
    
    def open_delete_collection_page(self):
        """Open the page to delete collections."""
        delete_collection_page = DeleteCollectionPage()
        self.wait_window(delete_collection_page)
    
    
    def open_add_author_page(self):
        """Open the page to add a new author."""
        add_author_page = AddAuthorPage(self.author_service)
        self.wait_window(add_author_page)
    
    def open_delete_author_page(self):
        """Open the page to delete authors."""
        delete_author_page = DeleteAuthorPage()
        self.wait_window(delete_author_page)

class AddThemePage(ctk.CTkToplevel):
    """Page for adding a new theme."""
    def __init__(self, theme_service : ThemeService):
        super().__init__()
        self.focus_set()
        self.grab_set()
        self.lift()
        self.geometry("400x145")
        self.title("Add Theme")
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.theme_service = theme_service
        
        ctk.CTkLabel(self, text="Name", anchor="w").pack(fill="x", padx=20)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(fill="x", padx=20)
        
        self.add_button = ctk.CTkButton(self, text="✅ Add Theme", command=self.confirm_action)
        self.add_button.pack(pady=10)
        self.cancel_button = ctk.CTkButton(self, text="❌ Cancel", fg_color="transparent", command=self.destroy)
        self.cancel_button.pack(pady=(0,10))
        self.bind("<Return>", lambda event: self.add_button.invoke())
        self.bind("<Escape>", lambda event: self.cancel_button.invoke())
        
        self.name_entry.focus_set()
        
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
    def __init__(self):
        """Page for deleting themes."""
        super().__init__()
        self.theme_service = ThemeService()
        self.themes = []

        self.focus_set()
        self.grab_set()
        self.lift()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.title("Delete Themes")
        self.geometry("500x600")

        title_label = ctk.CTkLabel(self, text="🗑️ Delete Themes", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(10, 5))

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=480, height=500)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.load_themes()

        self.bind("<Escape>", lambda event: self.destroy())

    def load_themes(self):
        """Load all themes and display them in the scrollable frame."""
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
                    text="🗑️ Delete",
                    fg_color="red",
                    hover_color="#cc0000",
                    width=100,
                    command=lambda t=theme: self.confirm_delete(t)
                )
                delete_btn.pack(side="right", padx=10)

        except Exception as e:
            PopUpMessage.pop_up(self, f"Error while loading : {str(e)}")

    def confirm_delete(self, theme):
        """Confirm the deletion of a theme."""
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Confirm deletion")
        confirm_window.geometry("300x150")
        confirm_window.grab_set()

        ctk.CTkLabel(
            confirm_window,
            text=f"Delete theme :\n'{theme.name}' ?",
            wraplength=250
        ).pack(pady=20)

        btn_frame = ctk.CTkFrame(confirm_window, fg_color="transparent")
        btn_frame.pack(pady=10)

        btn_yes = ctk.CTkButton(
            btn_frame,
            text="Yes",
            fg_color="red",
            hover_color="#cc0000",
            command=lambda: [
                self.delete_theme(theme),
                confirm_window.destroy()
            ]
        )
        btn_yes.pack(side="left", padx=10)

        btn_no = ctk.CTkButton(
            btn_frame,
            text="No",
            command=confirm_window.destroy
        )
        btn_no.pack(side="right", padx=10)
        confirm_window.bind("<Return>", lambda event: btn_yes.invoke())
        confirm_window.bind("<Escape>", lambda event: btn_no.invoke())

    def delete_theme(self, theme):
        """Delete the selected theme."""
        try:
            self.theme_service.delete_theme(theme.name)
            PopUpMessage.pop_up(self, f"✅ Theme deleted")
            self.load_themes()
        except Exception as e:
            PopUpMessage.pop_up(self, f"Error : {str(e)}")


class AddEditorPage(ctk.CTkToplevel):
    def __init__(self, editor_service : EditorService):
        """Page for adding a new editor.
        Initialize the add editor page.
        """
        super().__init__()

        self.focus_set()
        self.grab_set()
        self.lift()
        self.geometry("400x145")
        self.title("Add Editor")
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.editor_service = editor_service

        ctk.CTkLabel(self, text="Name", anchor="w").pack(fill="x", padx=20)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(fill="x", padx=20)
        
        self.add_button = ctk.CTkButton(self, text="✅ Add Editor", command=self.confirm_action)
        self.add_button.pack(pady=10)
        self.cancel_button = ctk.CTkButton(self, text="❌ Cancel", fg_color="transparent", command=self.destroy)
        self.cancel_button.pack(pady=(0,10))
        self.bind("<Return>", lambda event: self.add_button.invoke())
        self.bind("<Escape>", lambda event: self.cancel_button.invoke())
        
        self.name_entry.focus_set()
        
    def confirm_action(self):
        """Confirm the action of adding a new editor."""
        try:
            self.editor_service.add_editor(
                name=self.name_entry.get(),
            )

            PopUpMessage.pop_up(self, "Editor added ✅")
            self.destroy()

        except Exception as e:
            PopUpMessage.pop_up(self, str(e).lower())

class DeleteEditorPage(ctk.CTkToplevel):
    def __init__(self):
        """Page for deleting editors."""
        """Initialize the delete editor page."""
        super().__init__()

        self.focus_set()
        self.grab_set()
        self.lift()
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.editor_service = EditorService()
        self.editors = []

        self.title("Delete Editors")
        self.geometry("500x600")

        title_label = ctk.CTkLabel(self, text="🗑️ Delete Editors", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(10, 5))

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=480, height=500)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_editors()
        
        self.bind("<Escape>", lambda event: self.destroy())

    def load_editors(self):
        """Load all editors and display them in the scrollable frame."""
        """Load all editors from the editor service and display them."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            self.editors = self.editor_service.get_all()

            if not self.editors:
                empty_label = ctk.CTkLabel(self.scroll_frame, text="No editors available.", text_color="gray")
                empty_label.pack(pady=20)
                return

            for editor in self.editors:
                frame = ctk.CTkFrame(self.scroll_frame)
                frame.pack(fill="x", pady=5, padx=10)

                name_label = ctk.CTkLabel(frame, text=f"🏷️ {editor.name}", anchor="w")
                name_label.pack(side="left", padx=10, pady=5, fill="x", expand=True)

                delete_btn = ctk.CTkButton(
                    frame,
                    text="🗑️ Delete",
                    fg_color="red",
                    hover_color="#cc0000",
                    width=100,
                    command=lambda t=editor: self.confirm_delete(t)
                )
                delete_btn.pack(side="right", padx=10)

        except Exception as e:
            PopUpMessage.pop_up(self, f"Error while loading : {str(e)}")

    def confirm_delete(self, editor):
        """Confirm the deletion of an editor."""
        """Open a confirmation dialog to delete the selected editor."""
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Confirm deletion")
        confirm_window.geometry("300x150")
        confirm_window.grab_set()

        ctk.CTkLabel(
            confirm_window,
            text=f"Delete theme :\n'{editor.name}' ?",
            wraplength=250
        ).pack(pady=20)

        btn_frame = ctk.CTkFrame(confirm_window, fg_color="transparent")
        btn_frame.pack(pady=10)

        btn_yes = ctk.CTkButton(
            btn_frame,
            text="Yes",
            fg_color="red",
            hover_color="#cc0000",
            command=lambda: [
                self.delete_editor(editor),
                confirm_window.destroy()
            ]
        )
        btn_yes.pack(side="left", padx=10)

        btn_no = ctk.CTkButton(
            btn_frame,
            text="No",
            command=confirm_window.destroy
        )
        btn_no.pack(side="right", padx=10)
        
        confirm_window.bind("<Return>", lambda event: btn_yes.invoke())
        confirm_window.bind("<Escape>", lambda event: btn_no.invoke())

    def delete_editor(self, editor):
        """Delete the selected editor."""
        try:
            self.editor_service.delete_editor(editor.id)
            PopUpMessage.pop_up(self, f"✅ Editor deleted")
            self.load_editors()
        except Exception as e:
            PopUpMessage.pop_up(self, f"Error : {str(e)}")


class AddCollectionPage(ctk.CTkToplevel):
    def __init__(self, collection_service : CollectionService):
        """Page for adding a new collection."""
        super().__init__()
        self.focus_set()
        self.grab_set()
        self.lift()
        self.geometry("400x145")
        self.title("Add Collection")
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.collection_service = collection_service
        
        ctk.CTkLabel(self, text="Name", anchor="w").pack(fill="x", padx=20)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(fill="x", padx=20)
        
        self.add_button = ctk.CTkButton(self, text="✅ Add Collection", command=self.confirm_action)
        self.add_button.pack(pady=10)
        self.bind("<Return>", lambda event: self.add_button.invoke())
        self.cancel_button = ctk.CTkButton(self, text="❌ Cancel", fg_color="transparent", command=self.destroy)
        self.cancel_button.pack(pady=(0,10))
        self.bind("<Escape>", lambda event: self.cancel_button.invoke())
        
        self.name_entry.focus_set()
        
    def confirm_action(self):
        """Confirm the action of adding a new collection."""
        try:
            self.collection_service.add_collection(
                name=self.name_entry.get(),
            )

            PopUpMessage.pop_up(self, "Collection added ✅")
            self.destroy()

        except Exception as e:
            PopUpMessage.pop_up(self, str(e).lower())

class DeleteCollectionPage(ctk.CTkToplevel):
    def __init__(self):
        """Page for deleting collections."""
        """Initialize the delete collection page."""
        """This page allows users to delete existing collections."""
        """It displays a list of collections and provides an option to delete each one."""
        """Users can confirm the deletion of a collection through a confirmation dialog."""
        """After deletion, the list of collections is refreshed."""
        """The page also includes a title and a scrollable frame to display the collections."""
        """The page is designed to be modal, meaning it will block interaction with other windows until closed."""
        super().__init__()
        self.focus_set()
        self.grab_set()
        self.lift()
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.collection_service = CollectionService()
        self.collections = []

        self.title("Delete Collections")
        self.geometry("500x600")

        title_label = ctk.CTkLabel(self, text="🗑️ Delete Collections", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(10, 5))

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=480, height=500)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_collections()
        
        self.bind("<Escape>", lambda event: self.destroy())

    def load_collections(self):
        """Load all collections and display them in the scrollable frame."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            self.collections = self.collection_service.get_all()

            if not self.collections:
                empty_label = ctk.CTkLabel(self.scroll_frame, text="No collections available.", text_color="gray")
                empty_label.pack(pady=20)
                return

            for collection in self.collections:
                frame = ctk.CTkFrame(self.scroll_frame)
                frame.pack(fill="x", pady=5, padx=10)

                name_label = ctk.CTkLabel(frame, text=f"🏷️ {collection.name}", anchor="w")
                name_label.pack(side="left", padx=10, pady=5, fill="x", expand=True)

                delete_btn = ctk.CTkButton(
                    frame,
                    text="🗑️ Delete",
                    fg_color="red",
                    hover_color="#cc0000",
                    width=100,
                    command=lambda t=collection: self.confirm_delete(t)
                )
                delete_btn.pack(side="right", padx=10)

        except Exception as e:
            PopUpMessage.pop_up(self, f"Error while loading : {str(e)}")

    def confirm_delete(self, collection):
        """Open a confirmation dialog to delete the selected collection."""
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Confirm deletion")
        confirm_window.geometry("300x150")
        confirm_window.grab_set()

        ctk.CTkLabel(
            confirm_window,
            text=f"Delete theme :\n'{collection.name}' ?",
            wraplength=250
        ).pack(pady=20)

        btn_frame = ctk.CTkFrame(confirm_window, fg_color="transparent")
        btn_frame.pack(pady=10)

        btn_yes = ctk.CTkButton(
            btn_frame,
            text="Yes",
            fg_color="red",
            hover_color="#cc0000",
            command=lambda: [
                self.delete_collection(collection),
                confirm_window.destroy()
            ]
        )
        btn_yes.pack(side="left", padx=10)

        btn_no = ctk.CTkButton(
            btn_frame,
            text="No",
            command=confirm_window.destroy
        )
        btn_no.pack(side="right", padx=10)
        
        confirm_window.bind("<Return>", lambda event: btn_yes.invoke())
        confirm_window.bind("<Escape>", lambda event: btn_no.invoke())

    def delete_collection(self, collection):
        """Delete the selected collection."""
        try:
            self.collection_service.delete_collection_by_id(collection.id)
            PopUpMessage.pop_up(self, f"✅ Collection deleted")
            self.load_collections()
        except Exception as e:
            PopUpMessage.pop_up(self, f"Error : {str(e)}")


class AddAuthorPage(ctk.CTkToplevel):
    def __init__(self, author_service : AuthorService):
        """Page for adding a new author."""
        """Initialize the add author page."""
        """This page allows users to input the first and last name of a new author."""
        """It includes input fields for the first name and last name, along with buttons to confirm the action or cancel."""
        """When the confirm button is clicked, it attempts to add the author using the provided service."""
        self.focus_set()
        self.grab_set()
        self.lift()
        self.geometry("400x480")
        self.title("Add Author")
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.author_service = author_service
        
        ctk.CTkLabel(self, text="first name", anchor="w").pack(fill="x", padx=20)
        self.first_name_entry = ctk.CTkEntry(self)
        self.first_name_entry.pack(fill="x", padx=20)
        
        ctk.CTkLabel(self, text="Last name", anchor="w").pack(fill="x", padx=20)
        self.last_name_entry = ctk.CTkEntry(self)
        self.last_name_entry.pack(fill="x", padx=20)
        
        self.add_button = ctk.CTkButton(self, text="✅ Add Author", command=self.confirm_action)
        self.add_button.pack(pady=10)
        self.cancel_button = ctk.CTkButton(self, text="❌ Cancel", fg_color="transparent", command=self.destroy)
        self.cancel_button.pack(pady=(0,10))
        self.bind("<Return>", lambda event: self.add_button.invoke())
        self.bind("<Escape>", lambda event: self.cancel_button.invoke())
        
        self.first_name_entry.focus_set()
        
    def confirm_action(self):
        """Confirm the action of adding a new author."""
        try:
            self.author_service.add_author(
                first_name=self.first_name_entry.get(),
                last_name=self.last_name_entry.get()
            )

            PopUpMessage.pop_up(self, "Author added ✅")
            self.destroy()

        except Exception as e:
            PopUpMessage.pop_up(self, str(e).lower())

class DeleteAuthorPage(ctk.CTkToplevel):
    def __init__(self):
        """Page for deleting authors."""
        """Initialize the delete author page."""
        super().__init__()
        self.focus_set()
        self.grab_set()
        self.lift()
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.author_service = AuthorService()
        self.authors = []

        self.title("Delete authors")
        self.geometry("500x600")

        title_label = ctk.CTkLabel(self, text="🗑️ Delete Authors", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(10, 5))

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=480, height=500)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_authors()
        
        self.bind("<Escape>", lambda event: self.destroy())

    def load_authors(self):
        """Load all authors and display them in the scrollable frame."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            self.authors = self.author_service.get_all()

            if not self.authors:
                empty_label = ctk.CTkLabel(self.scroll_frame, text="No Authors available.", text_color="gray")
                empty_label.pack(pady=20)
                return

            for author in self.authors:
                frame = ctk.CTkFrame(self.scroll_frame)
                frame.pack(fill="x", pady=5, padx=10)

                author_names = " ".join([author.person.first_name, author.person.last_name]) 
                name_label = ctk.CTkLabel(frame, text=f"🏷️ {author_names}", anchor="w")
                name_label.pack(side="left", padx=10, pady=5, fill="x", expand=True)

                delete_btn = ctk.CTkButton(
                    frame,
                    text="🗑️ Delete",
                    fg_color="red",
                    hover_color="#cc0000",
                    width=100,
                    command=lambda t=author: self.confirm_delete(t)
                )
                delete_btn.pack(side="right", padx=10)

        except Exception as e:
            PopUpMessage.pop_up(self, f"Error while loading : {str(e)}")

    def confirm_delete(self, author):
        """Open a confirmation dialog to delete the selected author."""
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Confirm deletion")
        confirm_window.geometry("300x150")
        confirm_window.grab_set()

        ctk.CTkLabel(
            confirm_window,
            text=f"Delete author :\n'{author.person.last_name}' ?",
            wraplength=250
        ).pack(pady=20)

        btn_frame = ctk.CTkFrame(confirm_window, fg_color="transparent")
        btn_frame.pack(pady=10)

        btn_yes = ctk.CTkButton(
            btn_frame,
            text="Yes",
            fg_color="red",
            hover_color="#cc0000",
            command=lambda: [
                self.delete_author(author),
                confirm_window.destroy()
            ]
        )
        btn_yes.pack(side="left", padx=10)

        btn_no = ctk.CTkButton(
            btn_frame,
            text="No",
            command=confirm_window.destroy
        )
        btn_no.pack(side="right", padx=10)
        
        confirm_window.bind("<Return>", lambda event: btn_yes.invoke())
        confirm_window.bind("<Escape>", lambda event: btn_no.invoke())

    def delete_author(self, author):
        """Delete the selected author."""
        try:
            self.author_service.delete_author(author.id_author)
            PopUpMessage.pop_up(self, f"✅ Author deleted")
            self.load_authors()
        except Exception as e:
            PopUpMessage.pop_up(self, f"Error : {str(e)}")