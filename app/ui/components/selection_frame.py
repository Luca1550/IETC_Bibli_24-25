import customtkinter as ctk
from typing import TypeVar, Generic

T = TypeVar("T")

class SelectionFrame(ctk.CTkToplevel, Generic[T]):
    """
    A custom selection frame that allows users to select items from a list.
    It displays all items and allows users to add or remove selected items.
    It also provides a search functionality to filter items based on specified attributes.
    arguments:
    - parent: The parent widget for this frame.
    - title: The title of the selection frame.
    - all_items: A list of all items available for selection.
    - selected_items: A list of items that are currently selected.
    - display_model_method: A method to display the item in the UI.
    - attributes_to_search: A list of attributes to search for filtering items.
    - entry_to_update: An optional entry widget to update with selected items.
    - attributes_to_entry: An optional list of attributes to display in the entry widget.
    """
    def __init__(self, parent, title, all_items : list[T] , selected_items : list[T],  display_model_method, attributes_to_search, entry_to_update=None, attributes_to_entry = None, **kwargs):
        super().__init__(parent, **kwargs)

        self.geometry("400x535")
        self.focus_set()
        self.grab_set()
        self.lift()
        self.title("")
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.font=("default", 20)
        self.attributes_to_entry = attributes_to_entry
        self.entry_to_update = entry_to_update  

        label_title = ctk.CTkLabel(self, text=f"{title}", height=50, font=self.font)
        label_title.pack(fill="x", padx="15" )  

        self.all_items : list[T] = all_items
        self.old_selected_items : list[T] = selected_items
        self.selected_items : list[T] = list(selected_items) 
        self.display_model = display_model_method
        self.attributes_to_search = attributes_to_search

        self.all_items_widgets : dict[str, ctk.CTkFrame] = {}  
        self.selected_items_widgets : dict[str, ctk.CTkFrame] = {}  

        self.selected_items_parent_frame = ctk.CTkFrame(self, height=150, border_color="#1f6aa5", border_width=3)
        self.selected_items_parent_frame.pack(fill="both", padx="15", expand=True, pady="5")
        self.selected_items_parent_frame.pack_propagate(False)
        self.selected_items_parent_label = ctk.CTkLabel(self.selected_items_parent_frame, text=f"Selected items")
        self.selected_items_parent_label.pack(fill="x", padx="15", pady="5")
        self.selected_items_frame = ctk.CTkScrollableFrame(self.selected_items_parent_frame)
        self.selected_items_frame.pack(fill="both", padx="15", pady="10", expand=True)

        self.all_items_parent_frame = ctk.CTkFrame(self, border_color="#1f6aa5", border_width=3)
        self.all_items_parent_frame.pack(fill="both", pady="5", padx="15", expand=True)
        self.divider = ctk.CTkFrame(self.all_items_parent_frame, height=2, fg_color="transparent")
        self.divider.pack(fill="x", padx="15", pady="5")
        self.search_entry = ctk.CTkEntry(self.all_items_parent_frame, border_width=3, placeholder_text="Search")
        self.search_entry.pack(fill="x", padx="15")
        self.search_entry.bind("<KeyRelease>", lambda event: self.after(30, self._filter_all_items))
        self.all_items_frame = ctk.CTkScrollableFrame(self.all_items_parent_frame)
        self.all_items_frame.pack(fill="both", padx="15", pady="10", expand=True)

        self.confirm_button = ctk.CTkButton(self, text="Confirm", command=self._close)
        self.confirm_button.pack(fill="x", padx="15", pady="5")
        self._update_list()
        self._filter_all_items()

    def _filter_all_items(self):
        """
        Filters the items in the all_items_frame based on the search entry.
        It updates the displayed items based on the search value and the selected items.
        """
        search_value = self.search_entry.get().lower()

        new_research_values = [
            option for option in self.all_items 
            if option not in self.selected_items and 
            any(search_value in str(getattr(option, attr, "")).lower() for attr in self.attributes_to_search)
        ] if search_value else [option for option in self.all_items if option not in self.selected_items]

        for item in new_research_values:
            if item in self.selected_items_widgets:
                self.selected_items_widgets[item].pack(fill="both", expand=True, pady="2", padx="5")
            else:
                row_frame = ctk.CTkFrame(self.all_items_frame, border_width=2, height=35)
                row_frame.pack(fill="both", expand=True, pady="2", padx="5")
                row_frame.pack_propagate(False)

                label = ctk.CTkLabel(row_frame, text=self.display_model(item))
                label.pack(side="left", padx=10)

                add_button = ctk.CTkButton(row_frame, text="➕", width=30, command=lambda i=item: self._add_selection(i))
                add_button.pack(side="right", padx="2")

                self.selected_items_widgets[item] = row_frame 

        for item in list(self.selected_items_widgets.keys()):
            if item not in new_research_values:
                self.selected_items_widgets[item].pack_forget()

    def _add_selection(self, choice):
        """
        Adds a selected item to the list of selected items if it is not already selected.
        arguments:
        - choice: The item to be added to the selected items.
        """
        if choice and choice not in self.selected_items:
            self.selected_items.append(choice)
            self._update_list()
            self._filter_all_items()  

    def _delete_selection(self, choice):
        """
        Removes a selected item from the list of selected items.
        arguments:
        - choice: The item to be removed from the selected items.
        """
        if choice in self.selected_items:
            self.selected_items.remove(choice)
            self._update_list()
            self._filter_all_items()  

    def _update_list(self):
        """
        Updates the displayed list of selected items in the selected_items_frame.
        It creates a new row for each selected item and adds a delete button to remove the item from the selection.
        """
        for item in self.selected_items:
            if item in self.all_items_widgets:
                self.all_items_widgets[item].pack(fill="x", pady=2)
            else:
                row_frame = ctk.CTkFrame(self.selected_items_frame, border_width=2, height=35)
                row_frame.pack(fill="both", expand=True, pady="2", padx="5")
                row_frame.pack_propagate(False)

                label = ctk.CTkLabel(row_frame, text=self.display_model(item))
                label.pack(side="left", padx=10)

                delete_button = ctk.CTkButton(row_frame, text="➖", width=30, fg_color="red", command=lambda i=item: self._delete_selection(i))
                delete_button.pack(side="right", padx="2")

                self.all_items_widgets[item] = row_frame  

        for item in list(self.all_items_widgets.keys()):
            if item not in self.selected_items:
                self.all_items_widgets[item].pack_forget()

    def _close(self): 
        """
        Closes the selection frame.
        If the selected items have changed, it updates the old_selected_items list and the entry_to_update.
        """
        if self.old_selected_items != self.selected_items:
            self.old_selected_items[:] = self.selected_items
        if self.entry_to_update:
            self.entry_to_update.delete(0, "end")
            self.entry_to_update.insert(0, str(", ".join(" ".join(str(getattr(item, attr)) for attr in (self.attributes_to_search if self.attributes_to_entry is None else self.attributes_to_entry)) for item in self.selected_items)))
        self.destroy()