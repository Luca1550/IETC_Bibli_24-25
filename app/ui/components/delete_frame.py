import customtkinter as ctk
from .pop_up_message import PopUpMessage

class DeleteFrame(ctk.CTkToplevel):
    """ 
    DeleteFrame is a custom dialog for deleting items from a list.
    It displays a list of items and allows the user to delete them with confirmation.
    """
    def __init__(self, parent, title, items : list, display_model_method, delete_method, item_to_delete, entry_to_update, display_entry_to_update,**kwargs):
        super().__init__(parent, **kwargs)
        self.focus_set()
        self.grab_set()
        self.lift()
        self.title = ""
        self.protocol("WM_DELETE_WINDOW", self._close)
        self.geometry("500x600")

        self.items : list = items
        self.display_model_method = display_model_method
        self.all_items_widgets = {}
        self.delete_method = delete_method
        self.item_to_delete = item_to_delete
        self.entry_to_update = entry_to_update
        self.display_entry_to_update = display_entry_to_update
        title_label = ctk.CTkLabel(self, text=f"{title}", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(10, 5))

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=480, height=500)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_data()
        
        self.bind("<Escape>", lambda event:self.destroy())

    def load_data(self):
        """ Loads the items into the scrollable frame.
        It creates a row for each item with a label and a delete button."""
        for item in self.items:
            if item in self.all_items_widgets:
                self.all_items_widgets[item].pack(fill="x", pady=2)
            else:
                row_frame = ctk.CTkFrame(self.scroll_frame, border_width=2, height=35)
                row_frame.pack(fill="both", expand=True, pady="2", padx="5")
                row_frame.pack_propagate(False)

                label = ctk.CTkLabel(row_frame, text=self.display_model_method(item))
                label.pack(side="left", padx=10)

                delete_button = ctk.CTkButton(row_frame, text="Delete", width=30, fg_color="red", command=lambda i=item: self.confirm_delete(i))
                delete_button.pack(side="right", padx="2")

                self.all_items_widgets[item] = row_frame


    def _delete_item(self, item):
        """ Deletes the item from the list and calls the delete method."""
        try:
            self.delete_method(self.item_to_delete(item))
            PopUpMessage.pop_up(self, f"✅ {self.display_model_method(item)} deleted")
            self.items.remove(item)
            self.all_items_widgets[item].destroy()
            self.load_data()
        except Exception as e:
            PopUpMessage.pop_up(self, f"Error : {str(e)}")

    def confirm_delete(self, item):
        """ Opens a confirmation window to delete the item.
        If the user confirms, it calls the _delete"""
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Confirm deletion")
        confirm_window.geometry("300x150")
        confirm_window.grab_set()

        ctk.CTkLabel(
            confirm_window,
            text=f"Delete :\n'{self.display_model_method(item)}' ?",
            wraplength=250
        ).pack(pady=20)

        btn_frame = ctk.CTkFrame(confirm_window, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Yes",
            fg_color="red",
            hover_color="#cc0000",
            command=lambda: [
                self._delete_item(item),
                confirm_window.destroy(),
            ]
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="No",
            command=confirm_window.destroy
        ).pack(side="right", padx=10)

    def _close(self): 
        """
        Closes the delete frame.
        """
        if self.entry_to_update:
            self.entry_to_update.configure(text=self.display_entry_to_update(self.items))
        self.destroy()