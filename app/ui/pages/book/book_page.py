import customtkinter as ctk
from services import BookService,ThemeService,EditorService,CollectionService,AuthorService, ExemplarService
from services.models import BookDTO
from tools import Color
from ui.components import PopUpMessage
from .book_edit_page import BookEditPage
from .book_add_page import BookAddPage
from .book_config_page import BookConfigPage

class BookFrame(ctk.CTkFrame):
    """
        This class represents a frame that displays book details.
        It includes the book's title, publication date, price, collection,
        authors, editors, and themes. It also provides buttons to delete or edit the book.
    """
    def __init__(self, parent, book:BookDTO, delete_callback, edit_callback, exemplar_service : ExemplarService):
        """
            Initializes the BookFrame with the book details and callbacks for delete and edit actions.
            
            :param parent: The parent widget for this frame.
            :param book: An instance of BookDTO containing book details.
            :param delete_callback: A function to call when the delete button is pressed.
            :param edit_callback: A function to call when the edit button is pressed.
        """
        super().__init__(parent)
        self.book : BookDTO = book
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        self.exemplar_service = exemplar_service

        self.configure(
            border_width=0,  
        )
        self.pack_propagate(False)

        self.tag_font = ctk.CTkFont(size=13, weight="bold")
        self.title_font = ctk.CTkFont(size=14, weight="bold")

        border_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=15, border_width=5, border_color=Color.primary_color())
        border_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.top_frame = ctk.CTkFrame(border_frame, corner_radius=5, fg_color=Color.primary_color(), border_color=Color.primary_color())
        self.top_frame.pack(side="top", fill="x")

        self.left_frame = ctk.CTkFrame(border_frame)
        self.left_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(border_frame)
        self.right_frame.pack(side="right", fill="both", padx=10, pady=10)

        
        self.configure(corner_radius=10, border_width=1)
        self.setup_book_display()
    
    def setup_book_display(self):
        """
            Configure the display of book details in the frame.
        """

        # Button frame
        button_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        button_frame.pack(side="right", pady=5, padx=5)
        
        # Modify button
        if self.edit_callback:
            edit_btn = ctk.CTkButton(
                button_frame,
                text="✏️ Modify",
                width=100,
                command=lambda: self.edit_callback(self.book),
                fg_color="transparent",
                hover_color=(Color.hover_color(Color.secondary_color(), 30)),
                border_width=2,
                text_color="white",
            )
            edit_btn.pack(side="right", padx=(5, 0))

        # Delete button
        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Delete",
            fg_color="transparent",
            hover_color=(Color.hover_color(Color.error_color(), 30)),
            border_width=2,
            width=100,
            command=self.confirm_delete
        )
        delete_btn.pack(side="right", padx=(0, 5))
        

        # Book title
        title_label = ctk.CTkLabel(
            self.top_frame, 
            text=f"{self.book.title}", 
            font= ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            height=35
        )
        title_label.pack(side="left", anchor="w", padx=5,
            pady=5)
        
        # Date
        date_label = ctk.CTkLabel(
            self.top_frame, 
            text=f"Publication Date: {self.book.date}",
            corner_radius=25,
            height=25,
            fg_color=Color.background_color(),
            font = self.tag_font
        )
        date_label.pack(side="right", anchor="w", padx=5)
        
        # Collection
        collection_name = self.book.collection.name if self.book.collection else "No collection"
        collection_label = ctk.CTkLabel(
            self.top_frame, 
            text=f"Collection: {collection_name}",
            corner_radius=25,
            height=25,
            fg_color=Color.background_color(),
            font = self.tag_font
        )
        collection_label.pack(side="right", anchor="w", padx=5)

        # Price
        price_label = ctk.CTkLabel(
            self.top_frame, 
            text=f"Price: {self.book.price} €",
            corner_radius=25,
            height=25,
            fg_color=Color.background_color(),
            font = self.tag_font
        )
        price_label.pack(side="right", anchor="w", padx=5)
        
        # Author 
        author_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        author_frame.pack(fill="x", padx=5)
        author_title_label = ctk.CTkLabel(author_frame, text=f"Author(s)", font=self.title_font)
        author_title_label.pack(side="left", anchor="w", pady=2, padx=(5,5))
        separator = ctk.CTkFrame(self.left_frame, height=2, fg_color="gray")
        separator.pack(fill="x", padx=10, pady=5)
        for author in self.book.authors:
            author_label = ctk.CTkLabel(
                author_frame, 
                text=f"{author.person.first_name} {author.person.last_name}",
                corner_radius=25,
                height=25,
                fg_color=Color.primary_color(),
                font = self.tag_font
            )
            author_label.pack(side="left", anchor="w", pady=2, padx=5)
        # Editor 
        editor_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        editor_frame.pack(fill="x", padx=5)
        editor_title_label = ctk.CTkLabel(editor_frame, text=f"Editor(s)", font=self.title_font)
        editor_title_label.pack(side="left", anchor="w", pady=2, padx=(5,0))
        separator = ctk.CTkFrame(self.left_frame, height=2, fg_color="gray")
        separator.pack(fill="x", padx=10, pady=5)
        for editor in self.book.editors:
            editor_label = ctk.CTkLabel(
                editor_frame, 
                text=f"{editor.name}",
                corner_radius=25,
                height=25,
                fg_color=Color.primary_color(),
                font = self.tag_font
            )
            editor_label.pack(side="left", anchor="w",  pady=2, padx=5)
        
        # Theme
        theme_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        theme_frame.pack(fill="x", padx=5)
        theme_title_label = ctk.CTkLabel(theme_frame, text=f"Theme(s)", font=self.title_font)
        theme_title_label.pack(side="left", anchor="w", pady=2, padx=(5,0))
        for theme in self.book.themes:
            theme_label = ctk.CTkLabel(
                theme_frame, 
                text=f"{theme.name}",
                corner_radius=25,
                height=25,
                fg_color=Color.primary_color(),
                font = self.tag_font
            )
            theme_label.pack(side="left", anchor="w",  pady=2, padx=5)
        
        # Exemplar
        exemplars_frame = ctk.CTkScrollableFrame(self.right_frame, fg_color=None, scrollbar_button_color=Color.primary_color(), width=350)
        exemplars_frame.pack(fill="both", expand=True, padx=15)

        exemplars = self.exemplar_service.get_all_by_isbn(self.book.isbn)
        if exemplars:
            for exemplar in exemplars:
                exemplar_frame = ctk.CTkFrame(
                    exemplars_frame,
                    corner_radius=25,
                    height=25,
                    fg_color=Color.primary_color()
                    )
                exemplar_frame.pack(expand=True, fill="x", pady=5, padx=10)
                exemplar_label = ctk.CTkLabel(
                    exemplar_frame, 
                    text=f"Réf : {exemplar.id} | Localisation : {exemplar.location} | {exemplar.status.name.lower()}",
                    font = self.tag_font
                )
                exemplar_label.pack(side="left", pady=5, padx=15)
                status = ctk.CTkLabel(
                    exemplar_frame, 
                    text=f"",
                    font = self.tag_font,
                    fg_color=Color.status_color(int(exemplar.status.value)),
                    height=25,
                    width=25,
                    corner_radius=25
                )
                status.pack(side="right", pady=5, padx=5)
        else:
            exemplar_title_label = ctk.CTkLabel(exemplars_frame, text="No exemplar", font=self.title_font)
            exemplar_title_label.pack(anchor="w", pady=2, padx=5)
    
    def confirm_delete(self):
        """
            Open a confirmation window for book deletion.
        """
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Confirm deletion")
        confirm_window.geometry("300x150")
        confirm_window.resizable(False, False)
        confirm_window.grab_set()  # Modal
        
        # Window centering
        confirm_window.transient(self.winfo_toplevel())
        
        # Message
        message = ctk.CTkLabel(
            confirm_window,
            text=f"Are you sure you want to delete \n'{self.book.title}' ?",
            wraplength=250
        )
        message.pack(pady=20)
        
        # Buttons
        button_frame = ctk.CTkFrame(confirm_window, fg_color="transparent")
        button_frame.pack(pady=10)
        
        yes_btn = ctk.CTkButton(
            button_frame,
            text="Yes",
            fg_color="red",
            hover_color="#cc0000",
            command=lambda: [
                self.delete_callback(self.book),
                confirm_window.destroy()
            ]
        )
        yes_btn.pack(side="left", padx=10)
        
        no_btn = ctk.CTkButton(
            button_frame,
            text="No",
            command=confirm_window.destroy
        )
        no_btn.pack(side="right", padx=10)


class BookPage(ctk.CTkFrame):
    """
        This class represents the main page for managing books.
        It includes functionalities to add, edit, delete, and search for books.
        It also displays a list of books in a scrollable frame.
    """
    def __init__(self, parent):
        super().__init__(parent)
        
        self.editor_service = EditorService()
        self.author_service= AuthorService()
        self.collection_service = CollectionService()
        self.theme_service = ThemeService()
        self.book_service = BookService()
        self.exemplar_service = ExemplarService()
        self.books = []
        self.filtered_books = []        
        self.setup_ui()
        self.load_books()
        
    def setup_ui(self):
        """
            Configure the user interface for the book management page.
            It sets up the search bar, scrollable book list, and information display.
        """
        
        self.grid_rowconfigure(2, weight=1) 
        self.grid_columnconfigure(0, weight=1)
        
        # === Search zone ===
        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        search_frame.grid_columnconfigure(0, weight=1)
        search_frame.grid_columnconfigure(1, weight=0) 
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search by title...",
            height=35
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        add_btn = ctk.CTkButton(
            search_frame,
            text="➕ ADD",
            command=self.add_book,
            fg_color=Color.primary_color(),
            height=35
        )
        add_btn.grid(row=0, column=2, padx=(5, 10), pady=10)
        
        conf_btn = ctk.CTkButton(
            search_frame,
            text="✏️ CONFIG",
            command=self.conf_book,
            fg_color="#dd5019",
            hover_color="#cf714c",
            text_color="white",
            height=35
        )
        conf_btn.grid(row=0, column=1, padx=(5, 10), pady=10)
        
        
        # === Scrollable frame ===
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, scrollbar_button_color=Color.primary_color())
        self.scroll_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        # === Info ===
        info_frame = ctk.CTkFrame(self)
        info_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        self.info_label = ctk.CTkLabel(info_frame, text="", font=ctk.CTkFont(size=12))
        self.info_label.pack(pady=5)
    
    def load_books(self):
        """
            loads all books from the book service and displays them.
        """
        try:
            self.book_service = BookService()
            self.books = self.book_service.get_all()
            self.filtered_books = self.books.copy()
            self.display_books()
            self.update_info()
        except Exception as e:
            self.show_error(f"Error while loading : {str(e)}")
    
    def display_books(self):
        """
            displays the list of books in the scrollable frame.
        """
        # cleaning existing widgets in the scrollable frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        if not self.filtered_books:
            no_books_label = ctk.CTkLabel(
                self.scroll_frame,
                text="📚 No book found",
                font=ctk.CTkFont(size=16),
                text_color="gray",
            )
            no_books_label.pack(pady=50)
            return
        
        # displaying each book in a BookFrame
        for book in self.filtered_books:
            book_frame = BookFrame(
                self.scroll_frame,
                book,
                delete_callback=self.delete_book,
                edit_callback=self.edit_book,
                exemplar_service=self.exemplar_service
            )
            book_frame.pack(fill="x", padx=(0,10), pady=5)
    
    def edit_book(self,book):
        """
        open a page to edit a book
        """
        edit_page = BookEditPage(book=book,book_service=self.book_service,on_success=self.refresh)
        self.wait_window(edit_page)
        self.refresh()
        
    def add_book(self):
        """
        open a page to add a book
        """
        add_page = BookAddPage(book_service=self.book_service, author_service=self.author_service, exemplar_service=self.exemplar_service, on_success=self.refresh)
        self.wait_window(add_page)
        self.refresh()
    
    def conf_book(self):
        """
        open a page to configure books
        """
        add_page = BookConfigPage(theme_service=self.theme_service, editor_service=self.editor_service, collection_service=self.collection_service, author_service=self.author_service)
        self.wait_window(add_page)
        self.refresh()
    
    def delete_book(self, book):
        """
        Deletes a book and refreshes the book list.`
        """
        try:
            self.book_service.delete_book(book.isbn)
            self.load_books()
            self.show_success("Book successfully deleted !")
        except Exception as e:
            PopUpMessage(self, f"{e}")
    
    def on_search(self, event=None):
        """
            Handles the search functionality by filtering books based on the search query.
        """
        query = self.search_entry.get().lower().strip()
        
        if not query:
            self.filtered_books = self.books.copy()
        else:
            self.filtered_books = [
                book for book in self.books
                if query in book.title.lower()
            ]
        
        self.display_books()
        self.update_info()
    
    def update_info(self):
        """
            Updates the information label with the count of total and displayed books.
        """
        total = len(self.books)
        displayed = len(self.filtered_books)
        
        if total == displayed:
            info_text = f"📊 {total} book(s) total"
        else:
            info_text = f"📊 {displayed} book(s) displayed. {total} total"
        
        self.info_label.configure(text=info_text)
    
    def show_error(self, message):
        """
            shows an error message in the info label.
            waits for 3 seconds before clearing the message.
        """
        self.info_label.configure(text=f"❌ {message}", text_color="red")
        # self.after(3000, lambda: self.update_info())
    
    def show_success(self, message):
        """
            shows a success message in the info label.
            waits for 3 seconds before reverting to the normal state.
        """
        self.info_label.configure(text=f"✅ {message}", text_color="green")
        self.after(3000, lambda: self.update_info())
    
    def refresh(self):
        """
            Refreshes the book list by reloading the books from the service.
        """
        self.load_books()
        