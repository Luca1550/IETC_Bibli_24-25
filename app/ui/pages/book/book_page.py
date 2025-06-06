import customtkinter as ctk
import tkinter as tk
from services import BookService

class BookPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.book_service = BookService()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.setup_ui()
        
    def setup_ui(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self,width=200)
        self.scroll_frame.grid(row=0, column=0, sticky="nsew",pady=5,padx=5)

        # Exemple de contenu dans la scrollable
        # for i in range(30):
        #     label = ctk.CTkLabel(self.scroll_frame, text=f"Livre {i+1}")
        #     label.grid(row=i, column=0, padx=10, pady=5)
        all_books = self.book_service.get_all()
        for i, book in enumerate(all_books):
            book_text = f"{book.title} - {book.date} - {book.price} €"
            label = ctk.CTkLabel(self.scroll_frame, text=book_text)
            label.grid(row=i, column=0, padx=10, pady=5)