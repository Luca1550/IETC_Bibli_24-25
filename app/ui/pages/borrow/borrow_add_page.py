import customtkinter as ctk
from services import BookService, MemberService, BorrowService, ExemplarService
from ui.components import SelectionFrame, PopUpMessage

class BorrowAddPage(ctk.CTkToplevel):
    """
    A dialog for adding a new borrow record.
    It allows the user to select a book and a member, and then confirm the addition of the borrow record.
    """
    def __init__(self):
        super().__init__()
        self.focus_set()
        self.grab_set()
        self.lift()
        self.geometry("400x180")
        self.title(f"Add borrow")
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self._book_service : BookService = BookService()
        self._member_service : MemberService = MemberService()
        self._borrow_service : BorrowService = BorrowService()
        self._exemplar_service : ExemplarService = ExemplarService()
        self._book_selected = []
        self._member_selected = []

        self._book_without_status_borrowed = []
        for book in self._book_service.get_all():
            exemplars = self._exemplar_service.get_all_by_isbn(book.isbn)
            for exemplar in exemplars:
                if exemplar.status.value == 1 :
                    self._book_without_status_borrowed.append(book)
                    break

        ctk.CTkLabel(self, text="Books", anchor="w").pack(fill="x", padx=20)
        book_frame = ctk.CTkFrame(self, fg_color="transparent")
        book_frame.pack(fill="x", padx=20)
        self.book_entry = ctk.CTkEntry(book_frame, placeholder_text="No book")
        self.book_entry.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(book_frame, text="✏️", width=30, command=lambda: self.open_selection_frame(
            "Select book",
            self._book_without_status_borrowed,
            self._book_selected,
            lambda b: f"{b.isbn} | {b.title}",
            [lambda b: b.isbn, lambda b: b.title],
            self.book_entry
        )).pack(side="right", padx=(5, 0))
        self.book_entry.configure(state="disabled")

        ctk.CTkLabel(self, text="Member", anchor="w").pack(fill="x", padx=20)
        member_frame = ctk.CTkFrame(self, fg_color="transparent")
        member_frame.pack(fill="x", padx=20)
        self.member_entry = ctk.CTkEntry(member_frame, placeholder_text="No Member")
        self.member_entry.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(member_frame, text="✏️", width=30, command=lambda: self.open_selection_frame(
            "Select Member",
            self._member_service.get_all_members(),
            self._member_selected,
            lambda m: f"{m.person.first_name} {m.person.last_name}",
            [lambda m: m.person.first_name, lambda m: m.person.last_name],
            self.member_entry
        )).pack(side="right", padx=(5, 0))
        self.member_entry.configure(state="disabled")

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", pady=15, padx=20)
        add_button = ctk.CTkButton(button_frame, text="✅ Add", command=self.confirm)
        add_button.pack(side="right", pady=5, padx=5)
        cancel_button = ctk.CTkButton(button_frame, text="❌ Cancel", fg_color="transparent", command=self.destroy)
        cancel_button.pack(side="right", pady=5, padx=5)
        self.bind("<Return>", lambda event: add_button.invoke())
        self.bind("<Escape>", lambda event: cancel_button.invoke())

    def confirm(self):
        """
            Confirm the addition of a borrow record.
            It checks if the selected book and member are valid, and then adds the borrow record.
        """
        try:
            if not self._book_selected:
                raise Exception("At least one book must be selected.")

            if len(self._book_selected) > 1:
                raise Exception("No more than one book can be selected.")

            if not self._member_selected:
                raise Exception("At least one member must be selected.")

            if len(self._member_selected) > 1:
                raise Exception("No more than one member can be selected.")
            
            self._borrow_service.add_borrow(
                isbn=self._book_selected[0].isbn,
                id_member=self._member_selected[0].id_member
            )
        except Exception as e:
            l = PopUpMessage(self, message=f"{e}")
            self.wait_window(l)
            l.destroy()
            if "Borrow limit reached for this member" in str(e):
                self.destroy()
                return
            return
        s = PopUpMessage(self, message="Borrow added successfully!")
        self.wait_window(s)
        self.destroy()

    def open_selection_frame(self, title, all_items, selected_items, display_model_method, attributes_to_search, entry_to_update):
        """
        Opens a selection frame for choosing items from a list.
        """
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