import customtkinter as ctk
import tkinter as tk
from services import BookService

class BookPage(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        
        self.book_service = BookService()
        self.setup_ui()

    def setup_ui(self):
        pass