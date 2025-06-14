import customtkinter as ctk
from services import BookService,AuthorService,CollectionService,EditorService,ThemeService
from services.models import BookDTO
from ui.components import PopUpMessage,SelectionFrame
from .book_config_page import AddThemePage,AddCollectionPage,AddEditorPage,AddAuthorPage

class BookEditPage(ctk.CTkToplevel):
    """Page to edit a book's details."""
    def __init__(self, book:BookDTO, book_service: BookService ,on_success=None):
        """
        Initializes the BookEditPage.
        :param book: The book to edit.
        all info are separated by categories:
        - ISBN
        - Title
        - Date
        - Price
        - Collection
        - Author
        - Editor
        - Theme
        """
        self.book : BookDTO = book
        self.on_success = on_success
        self.book_service = book_service
        self.editor_service=EditorService()
        self.author_service=AuthorService()
        self.theme_service=ThemeService()
        self.collection_service=CollectionService()
        self.title(" ")
        self.geometry("500x600")
        
        ctk.CTkLabel(self, text="✏️ Edit Book", font=("Roboto", 18)).pack(pady=10)
        
        label_isbn_entry = ctk.CTkLabel(self, text="ISBN", anchor="w")
        label_isbn_entry.pack(fill="x", padx=20) 
        self.isbn_entry = ctk.CTkEntry(self)
        self.isbn_entry.pack(fill="x", padx=20)
        self.isbn_entry.insert(0, self.book.isbn)
        self.isbn_entry.configure(state="disabled")
        
        label_title_entry = ctk.CTkLabel(self, text="Title", anchor="w")
        label_title_entry.pack(fill="x", padx=20) 
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Title")
        self.title_entry.pack(fill="x", padx=20)
        self.title_entry.insert(0, self.book.title)
        
        label_date_entry = ctk.CTkLabel(self, text="Date", anchor="w")
        label_date_entry.pack(fill="x", padx=20) 
        self.date_entry = ctk.CTkEntry(self, placeholder_text="Date (YYYY-MM-DD)")
        self.date_entry.pack(fill="x", padx=20)
        self.date_entry.insert(0, str(self.book.date)) 
        
        label_price_entry = ctk.CTkLabel(self, text="Price €", anchor="w")
        label_price_entry.pack(fill="x", padx=20)
        self.price_entry = ctk.CTkEntry(self, placeholder_text="Price €")
        self.price_entry.pack(fill="x", padx=20)
        self.price_entry.insert(0, str(self.book.price))
        
        label_collection_entry = ctk.CTkLabel(self, text="Collection", anchor="w")
        label_collection_entry.pack(fill="x", padx=20)
        collection_frame = ctk.CTkFrame(self, fg_color="transparent")
        collection_frame.pack(fill="x", padx=20)
        self.collection_entry = ctk.CTkEntry(collection_frame, placeholder_text="Collection")
        self.collection_entry.pack(side="left", fill="x", expand=True)
        self.collection_entry.insert(0, str(self.book.collection.name if self.book.collection else "No collection"))
        self.selected_collection = [self.book.collection] if self.book.collection else []
        edit_collection_button = ctk.CTkButton(collection_frame, text="✏️", width=30, command=lambda:self.open_selection_frame(
            title="Collection update",
            all_items=self.collection_service.get_all(),
            selected_items=self.selected_collection,
            display_model_method=lambda collection: f"{collection.name}",
            attributes_to_search=[lambda collection: collection.name],
            entry_to_update=self.collection_entry
        ))
        edit_collection_button.pack(side="right", padx=(5, 0))
        self.collection_entry.configure(state="disabled")
        ctk.CTkButton(collection_frame,text="➕",width=30,command=self.open_add_collection_page).pack(side="right", padx=(5, 0))
        
        label_author_entry = ctk.CTkLabel(self, text="Author", anchor="w")
        label_author_entry.pack(fill="x", padx=20)
        author_frame = ctk.CTkFrame(self, fg_color="transparent")
        author_frame.pack(fill="x", padx=20)
        self.author_entry = ctk.CTkEntry(author_frame, placeholder_text="Author")
        self.author_entry.pack(side="left", fill="x", expand=True)
        author_names = ", ".join(" ".join([author.person.first_name, author.person.last_name]) for author in self.book.authors)
        self.author_entry.insert(0, str(author_names))
        edit_author_button = ctk.CTkButton(author_frame, text="✏️", width=30, command=lambda:self.open_selection_frame(
            title="Author update",
            all_items=self.author_service.get_all(),
            selected_items=self.book.authors,
            display_model_method=lambda author: f"{author.person.first_name} {author.person.last_name}",
            attributes_to_search=[
                lambda author: author.person.first_name,
                lambda author: author.person.last_name
                ],
            entry_to_update=self.author_entry
        ))
        edit_author_button.pack(side="right", padx=(5, 0))
        self.author_entry.configure(state="disabled")
        ctk.CTkButton(author_frame,text="➕",width=30,command=self.open_add_author_page).pack(side="right", padx=(5, 0))
        
        label_editor_entry = ctk.CTkLabel(self, text="Editor", anchor="w")
        label_editor_entry.pack(fill="x", padx=20)
        editor_frame = ctk.CTkFrame(self, fg_color="transparent")
        editor_frame.pack(fill="x", padx=20)
        self.editor_entry = ctk.CTkEntry(editor_frame, placeholder_text="Editor")
        self.editor_entry.pack(side="left", fill="x", expand=True)
        editor_names = ", ".join(editor.name for editor in self.book.editors)
        self.editor_entry.insert(0, str(editor_names))
        edit_editor_button = ctk.CTkButton(editor_frame, text="✏️", width=30, command=lambda:self.open_selection_frame(
            title="Editor update",
            all_items=self.editor_service.get_all(),
            selected_items=self.book.editors,
            display_model_method=lambda editor: f"{editor.name}",
            attributes_to_search=[lambda editor: {editor.name}],
            entry_to_update=self.editor_entry
        ))
        edit_editor_button.pack(side="right", padx=(5, 0))
        self.editor_entry.configure(state="disabled")
        ctk.CTkButton(editor_frame,text="➕",width=30,command=self.open_add_editor_page).pack(side="right", padx=(5, 0))
        
        label_theme_entry = ctk.CTkLabel(self, text="Theme", anchor="w")
        label_theme_entry.pack(fill="x", padx=20)
        theme_frame = ctk.CTkFrame(self, fg_color="transparent")
        theme_frame.pack(fill="x", padx=20)
        self.theme_entry = ctk.CTkEntry(theme_frame, placeholder_text="Theme")
        self.theme_entry.pack(side="left", fill="x", expand=True)
        theme_names = ", ".join(themes.name for themes in self.book.themes)
        self.theme_entry.insert(0, str(theme_names))
        edit_theme_button = ctk.CTkButton(theme_frame, text="✏️", width=30, command=lambda:self.open_selection_frame(
            title="Theme update",
            all_items=self.theme_service.get_all(),
            selected_items=self.book.themes,
            display_model_method=lambda theme: f"{theme.name}",
            attributes_to_search=[lambda theme: theme.name],
            entry_to_update=self.theme_entry
        ))
        edit_theme_button.pack(side="right", padx=(5, 0))
        self.theme_entry.configure(state="disabled")
        ctk.CTkButton(theme_frame,text="➕",width=30,command=self.open_add_theme_page).pack(side="right", padx=(5, 0))
        
        
        ctk.CTkButton(self, text="✅ Save", command=self.confirm_action).pack(pady=10)
        ctk.CTkButton(self, text="❌ Cancel", fg_color="transparent", command=self.destroy).pack()
        
    def open_selection_frame(self,title,all_items,selected_items,display_model_method,attributes_to_search,entry_to_update,attributes_to_entry=None):
        """
            opens a selection frame to choose items from a list.
        """
        selection_frame = SelectionFrame(
            self,
            title,
            all_items,
            selected_items,
            display_model_method,
            attributes_to_search,
            entry_to_update,
            attributes_to_entry
        )
        self.wait_window(selection_frame)
        
    def open_add_theme_page(self):
        """Opens the AddThemePage to add a new theme."""
        add_theme_page = AddThemePage(self.theme_service)
        self.wait_window(add_theme_page)
    
    def open_add_editor_page(self):
        """Opens the AddEditorPage to add a new editor."""
        add_editor_page = AddEditorPage(self.editor_service)
        self.wait_window(add_editor_page)
    
    def open_add_collection_page(self):
        """Opens the AddCollectionPage to add a new collection."""
        add_collection_page = AddCollectionPage(self.collection_service)
        self.wait_window(add_collection_page)
    
    def open_add_author_page(self):
        """Opens the AddAuthorPage to add a new author."""
        add_author_page = AddAuthorPage(self.author_service)
        self.wait_window(add_author_page)

    def confirm_action(self):
        """
        Validates the input fields and adds a new person using the BookService.
        If the book is added successfully, the page is closed.
        If there is an error, a pop-up message is displayed with the error details.
        """
        try:
            if not self.selected_collection:
                if len(self.selected_collection)>1:
                    raise Exception ("A book can only have one collection.")
            self.book_service.update_by_parameter(
                isbn=self.isbn_entry.get(),
                title=self.title_entry.get(),
                date=self.date_entry.get(),
                price=self.price_entry.get(),
                collection=self.selected_collection[0] if self.selected_collection else None,
                authors=self.book.authors,
                themes=self.book.themes,
                editors=self.book.editors
            )
            
            # if self.on_success:
            #     self.on_success()
            PopUpMessage.pop_up(self,f"Book updated ✅")
            self.destroy()
        except Exception as e :
                PopUpMessage.pop_up(self,str(e).lower())
        
    
