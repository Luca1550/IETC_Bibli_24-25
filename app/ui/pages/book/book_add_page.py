import customtkinter as ctk
from services import BookService, AuthorService, CollectionService, EditorService, ThemeService, ExemplarService
from ui.components import PopUpMessage, SelectionFrame
from ui.pages import AddExemplarPage
from tools import Color
from .book_config_page import AddThemePage,AddCollectionPage,AddEditorPage,AddAuthorPage

class BookAddPage(ctk.CTkToplevel):
    """
        page for adding a new book to the library.
        It allows the user to input book details such as ISBN, title, date, price,
        and select associated authors, editors, themes, and collections.
        It also provides options to add new authors, editors, themes, and collections.
    """
    def __init__(self, book_service: BookService, exemplar_service : ExemplarService,author_service : AuthorService, on_success=None):
        """
        Initialize the book add page.
        attributes are seprarated by a blank line for better readability.
        """
        super().__init__()
        self.grab_set()
        self.focus_set()
        self.lift
        self.book_service = book_service
        self.author_service = author_service
        self.collection_service = CollectionService()
        self.editor_service = EditorService()
        self.theme_service = ThemeService()
        self.exemplar_service = exemplar_service
        self.on_success = on_success

        self.title(" ")
        self.geometry("500x600")


        self.selected_collection = []
        self.selected_authors = []
        self.selected_editors = []
        self.selected_themes = []

        ctk.CTkLabel(self, text="📚 Add Book", font=("Roboto", 18)).pack(pady=10)

        ctk.CTkLabel(self, text="ISBN", anchor="w").pack(fill="x", padx=20)
        self.isbn_entry = ctk.CTkEntry(self, placeholder_text="ISBN")
        self.isbn_entry.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Title", anchor="w").pack(fill="x", padx=20)
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Title")
        self.title_entry.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Date (YYYY-MM-DD)", anchor="w").pack(fill="x", padx=20)
        self.date_entry = ctk.CTkEntry(self, placeholder_text="Date")
        self.date_entry.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Price €", anchor="w").pack(fill="x", padx=20)
        self.price_entry = ctk.CTkEntry(self, placeholder_text="Price €")
        self.price_entry.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Collection", anchor="w").pack(fill="x", padx=20)
        collection_frame = ctk.CTkFrame(self, fg_color="transparent")
        collection_frame.pack(fill="x", padx=20)
        self.collection_entry = ctk.CTkEntry(collection_frame, placeholder_text="No collection")
        self.collection_entry.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(collection_frame, text="✏️", width=30, command=lambda: self.open_selection_frame(
            lambda c: c.name,
            [lambda c: c.name],
            self.collection_entry
        )).pack(side="right", padx=(5, 0))
        self.collection_entry.configure(state="disabled")
        ctk.CTkButton(collection_frame,text="➕",width=30,command=self.open_add_collection_page).pack(side="right", padx=(5, 0))

        ctk.CTkLabel(self, text="Authors", anchor="w").pack(fill="x", padx=20)
        author_frame = ctk.CTkFrame(self, fg_color="transparent")
        author_frame.pack(fill="x", padx=20)
        self.author_entry = ctk.CTkEntry(author_frame, placeholder_text="No author")
        self.author_entry.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(author_frame, text="✏️", width=30, command=lambda: self.open_selection_frame(
            "Select Authors",
            self.author_service.get_all(),
            self.selected_authors,
            lambda a: f"{a.person.first_name} {a.person.last_name}",
            [lambda a: a.person.first_name, lambda a: a.person.last_name],
            self.author_entry
        )).pack(side="right", padx=(5, 0))
        self.author_entry.configure(state="disabled")
        ctk.CTkButton(author_frame,text="➕",width=30,command=self.open_add_author_page).pack(side="right", padx=(5, 0))

        ctk.CTkLabel(self, text="Editors", anchor="w").pack(fill="x", padx=20)
        editor_frame = ctk.CTkFrame(self, fg_color="transparent")
        editor_frame.pack(fill="x", padx=20)
        self.editor_entry = ctk.CTkEntry(editor_frame, placeholder_text="No editor")
        self.editor_entry.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(editor_frame, text="✏️", width=30, command=lambda: self.open_selection_frame(
            "Select Editors",
            self.editor_service.get_all(),
            self.selected_editors,
            lambda e: e.name,
            [lambda e: e.name],
            self.editor_entry
        )).pack(side="right", padx=(5, 0))
        self.editor_entry.configure(state="disabled")
        ctk.CTkButton(editor_frame,text="➕",width=30,command=self.open_add_editor_page).pack(side="right", padx=(5, 0))

        ctk.CTkLabel(self, text="Themes", anchor="w").pack(fill="x", padx=20)
        theme_frame = ctk.CTkFrame(self, fg_color="transparent")
        theme_frame.pack(fill="x", padx=20)
        self.theme_entry = ctk.CTkEntry(theme_frame, placeholder_text="No theme")
        self.theme_entry.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(theme_frame, text="✏️", width=30, command=lambda: self.open_selection_frame(
            "Select Themes",
            self.theme_service.get_all(),
            self.selected_themes,
            lambda t: t.name,
            [lambda t: t.name],
            self.theme_entry
        )).pack(side="right", padx=(5, 0))
        self.theme_entry.configure(state="disabled")
        ctk.CTkButton(theme_frame,text="➕",width=30,command=self.open_add_theme_page).pack(side="right", padx=(5, 0))

        ctk.CTkButton(self, text="✅ Add Book", command=self.confirm_action).pack(pady=10)
        ctk.CTkButton(self, text="❌ Cancel", fg_color="transparent", command=self.destroy).pack()



    def open_selection_frame(self, title, all_items, selected_items, display_model_method, attributes_to_search, entry_to_update):
        """Open a selection frame for choosing items from a list."""
        selection_frame = SelectionFrame(
            self,
            title,
            all_items,
            selected_items,
            display_model_method,
            attributes_to_search,
            entry_to_update
        )
        self.wait_window(selection_frame)
        
    def open_add_theme_page(self):
        """Open the page to add a new theme."""
        add_theme_page = AddThemePage(self.theme_service)
        self.wait_window(add_theme_page)
    
    def open_add_editor_page(self):
        """Open the page to add a new editor."""
        add_editor_page = AddEditorPage(self.editor_service)
        self.wait_window(add_editor_page)
    
    def open_add_collection_page(self):
        """Open the page to add a new collection."""
        add_collection_page = AddCollectionPage(self.collection_service)
        self.wait_window(add_collection_page)
    
    def open_add_author_page(self):
        """Open the page to add a new author."""
        add_author_page = AddAuthorPage(self.author_service)
        self.wait_window(add_author_page)

    def open_add_exemplar_page(self, book):
        """Open the page to add a new exemplar."""
        add_exemplar_page = AddExemplarPage(book, self.exemplar_service)
        self.wait_window(add_exemplar_page)
        self.destroy()
        

    def pop_up_add_exemplar(self, book):
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Choice Box")
        confirm_window.geometry("300x150")
        confirm_window.grab_set()

        ctk.CTkLabel(
            confirm_window,
            text=f"Would you like to add an exemplar?",
            wraplength=250
        ).pack(pady=20)

        btn_frame = ctk.CTkFrame(confirm_window, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Yes",
            command=lambda :   self.open_add_exemplar_page(book)
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="No",
            command=lambda: [
                confirm_window.destroy(),
            ]
        ).pack(side="right", padx=10)
        


    def confirm_action(self):
        """Confirm the action of adding a book with the provided details."""
        try:
            if len(self.selected_collection) > 1:
                raise Exception("A book can only have one collection.")

            book = self.book_service.add_book(
                isbn=self.isbn_entry.get(),
                title=self.title_entry.get(),
                date=self.date_entry.get(),
                price=self.price_entry.get(),
                collection=self.selected_collection[0] if self.selected_collection else None,
                authors=self.selected_authors,
                editors=self.selected_editors,
                themes=self.selected_themes
            )

            PopUpMessage.pop_up(self, "Book added ✅")
            self.pop_up_add_exemplar(book)

        except Exception as e:
            PopUpMessage.pop_up(self, str(e).lower())
