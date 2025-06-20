
import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from services import LibraryService
from ui.components import PopUpMessage

class LibraryPage(ctk.CTkFrame):
    """Page to manage library parameters.
    This page allows the user to view and update library parameters or add a new library if none exists."""
    def __init__(self, parent):
        """
        Initializes the LibraryPage frame.
        :param parent: The parent widget to which this frame will be attached.
        """
        super().__init__(parent)
        
        self.library_service = LibraryService()
        self.libraries = []
        self.setup_ui()
        

    def setup_ui(self):
        """
        Sets up the user interface for the LibraryPage.

        Configures the grid layout for the main panel to take up the entire window
        and adapts to resizing. Initializes the main panel and sets its layout.
        Displays the title "Library" at the top of the form.

        Depending on the number of library parameters retrieved, either
        initializes the form for updating library parameters or adding a new library.
        Displays an error message if more than one library is found.
        """

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  

        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        

        self.form_title = ctk.CTkLabel(self.main_panel, text="Library Configuration", font=ctk.CTkFont(size=18, weight="bold"))
        self.form_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self.paramlib = self.library_service.get_library_parameters()

        if len(self.paramlib) ==1:
            self.lib_form()
        elif len(self.paramlib) ==0:
            self.add_form()
        else:
            PopUpMessage.pop_up(self, "error: You cannot have more than one library, please call your admin")
        self.main_panel.grid_columnconfigure(1, weight=1)  

    def lib_form(self):
        """
        Displays the form to update library parameters if a library exists.
        :param self: The instance of the class.
        :return: None
        """
        
        if self.paramlib:

            lib_params=self.paramlib[0]
            
            self.entries={}
            for i,(key, value) in enumerate(lib_params.__dict__.items(),start=1):
                if key != "id":
                    label_txt= key.replace("_"," ").capitalize()
                
                    self.label= ctk.CTkLabel(self.main_panel,text=label_txt)
                    self.label.grid(row=i, column=0, sticky="w", padx=1, pady=1)

                    self.label_entry = ctk.CTkEntry(self.main_panel)
                    self.label_entry.grid(row=i, column=1, sticky="ew", pady=1)
                    self.label_entry.insert(0, str(value))
                    self.entries[key] = self.label_entry
                    row_index = i

        self.save_button = ctk.CTkButton(self.main_panel, text="Save", command=self.update_libraries)
        self.save_button.grid(row=row_index+1, column=0, columnspan=2, pady=10)
    def update_libraries(self):
        """
        Updates the library parameters from the form values and calls the update_library method on the library service
        with the updated parameters.
        
        """
        updated_param={}
        updated_param["id"] =self.paramlib[0].id
        
        for key, value in self.entries.items():
            val = value.get()
            if key in ["fine_per_day", "subscribe_amout", "borrow_price_with_sub", "borrow_price_without_sub"]:
                updated_param[key] = float(val)
            elif key in ["limit_borrow", "borrow_delay","limit_reservation"]:
                updated_param[key] = int(val)
            else:
                updated_param[key] = val
        
        self.library_service.update_library(**updated_param)
        
    def add_form(self):
        
        
        """
        Creates the form to add a new library.
        """
        self.label_name= ctk.CTkLabel(self.main_panel,text='Name')
        self.label_name.grid(row=1, column=0, sticky="w", padx=1, pady=1)
        self.entry_name = ctk.CTkEntry(self.main_panel)
        self.entry_name.grid(row=1, column=1, sticky="ew", pady=1)
        
        self.label_fpd= ctk.CTkLabel(self.main_panel,text='Fine per day')
        self.label_fpd.grid(row=2, column=0, sticky="w", padx=1, pady=1)
        self.entry_fpd = ctk.CTkEntry(self.main_panel)
        self.entry_fpd.grid(row=2, column=1, sticky="ew", pady=1)
        
        self.label_sa= ctk.CTkLabel(self.main_panel,text='Subscribe amount')
        self.label_sa.grid(row=3, column=0, sticky="w", padx=1, pady=1)
        self.entry_sa = ctk.CTkEntry(self.main_panel)
        self.entry_sa.grid(row=3, column=1, sticky="ew", pady=1)
        
        self.label_lb= ctk.CTkLabel(self.main_panel,text='Limit borrow')
        self.label_lb.grid(row=4, column=0, sticky="w", padx=1, pady=1)
        self.entry_lb = ctk.CTkEntry(self.main_panel)
        self.entry_lb.grid(row=4, column=1, sticky="ew", pady=1)
        
        self.label_bpws= ctk.CTkLabel(self.main_panel,text='Borrow price with sub')
        self.label_bpws.grid(row=5, column=0, sticky="w", padx=1, pady=1)
        self.entry_bpws = ctk.CTkEntry(self.main_panel)
        self.entry_bpws.grid(row=5, column=1, sticky="ew", pady=1)
        
        self.label_bpwts= ctk.CTkLabel(self.main_panel,text='Borrow price without sub')
        self.label_bpwts.grid(row=6, column=0, sticky="w", padx=1, pady=1)
        self.entry_bpwts = ctk.CTkEntry(self.main_panel)
        self.entry_bpwts.grid(row=6, column=1, sticky="ew", pady=1)
        
        self.label_bd= ctk.CTkLabel(self.main_panel,text='Borrow delay')
        self.label_bd.grid(row=7, column=0, sticky="w", padx=1, pady=1)
        self.entry_bd = ctk.CTkEntry(self.main_panel)
        self.entry_bd.grid(row=7, column=1, sticky="ew", pady=1)
        
        self.label_lr= ctk.CTkLabel(self.main_panel,text='Limit reservation')
        self.label_lr.grid(row=9, column=0, sticky="w", padx=1, pady=1)
        self.entry_lr = ctk.CTkEntry(self.main_panel)
        self.entry_lr.grid(row=9, column=1, sticky="ew", pady=1)

        self.add_button = ctk.CTkButton(self.main_panel, text="Add",command=self.add_library)
        self.add_button.grid(row=10, column=0, columnspan=2, pady=10)

    def add_library(self):
        """
        Collects input values from the form fields and attempts to add a new library using the LibraryService.
        
        Retrieves the name, fine per day, subscription amount, limit on borrowable items,
        borrowing price with and without subscription, borrowing delay for the library logo
        from user input. Converts the numerical values to the appropriate types.
        
        Calls the add_library method of the LibraryService with the collected parameters.
        Displays a success pop-up message if the library is added successfully.
        If any input errors occur, a pop-up message is displayed with the error details.
        """

        try:
            name = self.entry_name.get()
            fine_per_day = float(self.entry_fpd.get())
            subscribe_amount = float(self.entry_sa.get())
            limit_borrow = int(self.entry_lb.get())
            borrow_with_sub = float(self.entry_bpws.get())
            borrow_without_sub = float(self.entry_bpwts.get())
            borrow_delay = int(self.entry_bd.get())
            limit_reservation = int(self.entry_lr.get())
            newlib=self.library_service.add_library(name,fine_per_day,subscribe_amount,limit_borrow,borrow_with_sub,borrow_without_sub,borrow_delay,limit_reservation)
            if isinstance(newlib, str):
                PopUpMessage.pop_up(self, newlib)
            else:
                PopUpMessage.pop_up(self, "Library added successfully!")
                self.destroy()
                
        except ValueError as e:
            PopUpMessage.pop_up(self, f"Input error: {e}")


