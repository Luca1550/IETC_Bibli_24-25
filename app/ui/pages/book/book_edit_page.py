import customtkinter as ctk
from services import BookService
from ui.components import PopUpMessage

class BookEditPage(ctk.CTkToplevel):
    def __init__(self, book, on_success=None):
        super().__init__()
        self.book = book
        self.on_success = on_success  # callback pour rafraîchir BookPage
        self.book_service = BookService()
        self.title("✏️ Edit Book")
        self.geometry("500x400")
        
        ctk.CTkLabel(self, text="✏️ Edit Book", font=("Roboto", 18)).pack(pady=10)
        
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Title")
        self.title_entry.pack(fill="x", padx=20, pady=5)
        self.title_entry.insert(0, book.title)
        
        self.date_entry = ctk.CTkEntry(self, placeholder_text="Date (YYYY-MM-DD)")
        self.date_entry.pack(fill="x", padx=20, pady=5)
        self.date_entry.insert(0, str(book.date))  # ou book.date.strftime("%Y-%m-%d")
        
        self.price_entry = ctk.CTkEntry(self, placeholder_text="Price")
        self.price_entry.pack(fill="x", padx=20, pady=5)
        self.price_entry.insert(0, str(book.price))
        
        # Ajoute d'autres champs ici si nécessaire (collection, auteurs, etc.)
        
        ctk.CTkButton(self, text="✅ Save", command=self.update_book).pack(pady=10)
        ctk.CTkButton(self, text="❌ Cancel", fg_color="transparent", command=self.destroy).pack()

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
