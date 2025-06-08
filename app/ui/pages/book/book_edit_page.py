import customtkinter as ctk
from services import BookService
from services.models import BookDTO
from ui.components import PopUpMessage

class BookEditPage(ctk.CTkToplevel):
    def __init__(self, book:BookDTO, on_success=None):
        super().__init__()
        self.book : BookDTO = book
        self.on_success = on_success  # callback pour rafraîchir BookPage
        self.book_service = BookService()
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
        self.collection_entry.insert(0, str(self.book.collection.name))
        edit_collection_button = ctk.CTkButton(collection_frame, text="✏️", width=30, command=None)
        edit_collection_button.pack(side="right", padx=(5, 0))
        
        label_collection_entry = ctk.CTkLabel(self, text="Author", anchor="w")
        label_collection_entry.pack(fill="x", padx=20)
        author_frame = ctk.CTkFrame(self, fg_color="transparent")
        author_frame.pack(fill="x", padx=20)
        self.author_entry = ctk.CTkEntry(author_frame, placeholder_text="Author")
        self.author_entry.pack(side="left", fill="x", expand=True)
        author_names = ", ".join(" ".join([author.person.first_name, author.person.last_name]) for author in self.book.authors)
        self.author_entry.insert(0, str(author_names))
        edit_author_button = ctk.CTkButton(author_frame, text="✏️", width=30, command=None)
        edit_author_button.pack(side="right", padx=(5, 0))
        
        label_editor_entry = ctk.CTkLabel(self, text="Editor", anchor="w")
        label_editor_entry.pack(fill="x", padx=20)
        editor_frame = ctk.CTkFrame(self, fg_color="transparent")
        editor_frame.pack(fill="x", padx=20)
        self.editor_entry = ctk.CTkEntry(editor_frame, placeholder_text="Editor")
        self.editor_entry.pack(side="left", fill="x", expand=True)
        self.editor_entry.insert(0, str(self.book.price))
        edit_editor_button = ctk.CTkButton(editor_frame, text="✏️", width=30, command=None)
        edit_editor_button.pack(side="right", padx=(5, 0))
        
        label_theme_entry = ctk.CTkLabel(self, text="Theme", anchor="w")
        label_theme_entry.pack(fill="x", padx=20)
        theme_frame = ctk.CTkFrame(self, fg_color="transparent")
        theme_frame.pack(fill="x", padx=20)
        self.theme_entry = ctk.CTkEntry(theme_frame, placeholder_text="Theme")
        self.theme_entry.pack(side="left", fill="x", expand=True)
        self.theme_entry.insert(0, str(self.book.price))
        edit_theme_button = ctk.CTkButton(theme_frame, text="✏️", width=30, command=None)
        edit_theme_button.pack(side="right", padx=(5, 0))
        
        # Ajoute d'autres champs ici si nécessaire (collection, auteurs, etc.)
        
        ctk.CTkButton(self, text="✅ Save", command=self.confirm_action).pack(pady=10)
        ctk.CTkButton(self, text="❌ Cancel", fg_color="transparent", command=self.destroy).pack()

    def confirm_action(self):
        """
        Validates the input fields and adds a new person using the BookService.
        If the book is added successfully, the page is closed.
        If there is an error, a pop-up message is displayed with the error details.
        """
        try: 
            self.book_service.update_by_parameter(
                isbn=self.isbn_entry.get(),
                title=self.title_entry.get(),
                date=self.date_entry.get(),
                price=self.price_entry.get(),
                collection=self.collection,
                authors=self.authors,
                themes=self.themes,
                editors=self.editors
            )
            
            PopUpMessage.pop_up(self,f"Book updated ✅")
            self.destroy()
        except Exception as e :
                PopUpMessage.pop_up(self,e)
        
    def update_book(self):
        try:
            title = self.title_entry.get().strip()
            date_str = self.date_entry.get().strip()
            price = float(self.price_entry.get().strip())

            from datetime import datetime
            date = datetime.strptime(date_str, "%Y-%m-%d")
            
            # Tu peux remplacer ici les valeurs None par les vraies (auteurs, collection...)
            updated = self.book_service.update_by_parameter(
                isbn=self.book.isbn,
                title=title,
                date=date,
                price=price,
                collection=None,
                authors=[],
                themes=[],
                editors=[]
            )

            PopUpMessage.pop_up(self, "✅ Book updated successfully")
            if self.on_success:
                self.on_success()  # callback pour rafraîchir la liste
            self.destroy()

        except Exception as e:
            PopUpMessage.pop_up(self, f"❌ Error: {str(e)}")
