import customtkinter as ctk
from services.models import BookDTO
from services import ExemplarService
from ui.components import PopUpMessage

class AddExemplarPage(ctk.CTkToplevel):
    def __init__(self, book : BookDTO, exemplar_service : ExemplarService):
        super().__init__()
        self.focus_set()
        self.grab_set()
        self.lift()
        self.geometry("400x250")
        self.title(f"Add exemplar for {book.title}")
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.exemplar_service = exemplar_service
        self.book = book
        
        ctk.CTkLabel(self, text="Location", anchor="w").pack(fill="x", padx=20)
        self.location_entry = ctk.CTkEntry(self)
        self.location_entry.pack(fill="x", padx=20)

        ctk.CTkButton(self, text="✅ Add exemplar", command=self.confirm_action).pack(pady=10)
        ctk.CTkButton(self, text="➕ Add exemplar and continue", command=self.confirm_and_continue).pack(pady=10)
        ctk.CTkButton(self, text="❌ Cancel", fg_color="transparent", command=self.destroy).pack(pady=(0,10))


    def confirm_and_continue(self):
        try:
            self.exemplar_service.add_exemplar(
                isbn=self.book.isbn,
                location=self.location_entry.get(),
                status=1
            )

            PopUpMessage.pop_up(self, "Exemplar added ✅")
            self.location_entry.delete(0, "end") 
        except Exception as e:
            PopUpMessage.pop_up(self, str(e).lower())

    def confirm_action(self):
        try:
            self.exemplar_service.add_exemplar(
                isbn=self.book.isbn,
                location=self.location_entry.get(),
                status=1
            )

            PopUpMessage.pop_up(self, "Exemplar added ✅")
            self.destroy()

        except Exception as e:
            PopUpMessage.pop_up(self, str(e).lower())