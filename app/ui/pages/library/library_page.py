
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
        library =self.paramlib[0]
        self.label_name= ctk.CTkLabel(self.main_panel,text='Name')
        self.label_name.grid(row=1, column=0, sticky="w", padx=1, pady=1)
        self.entry_name = ctk.CTkEntry(self.main_panel,placeholder_text="Name of the library")
        self.entry_name.grid(row=1, column=1, sticky="ew", pady=1)
        
        self.label_fpd= ctk.CTkLabel(self.main_panel,text='Daily overdue fee')
        self.label_fpd.grid(row=2, column=0, sticky="w", padx=1, pady=1)
        self.entry_fpd = ctk.CTkEntry(self.main_panel,placeholder_text="Amout (in €) a user will be fined per day if a book is late to be returned")
        self.entry_fpd.grid(row=2, column=1, sticky="ew", pady=1)
        
        self.label_sa= ctk.CTkLabel(self.main_panel,text='Subscription price')
        self.label_sa.grid(row=3, column=0, sticky="w", padx=1, pady=1)
        self.entry_sa = ctk.CTkEntry(self.main_panel,placeholder_text="€")
        self.entry_sa.grid(row=3, column=1, sticky="ew", pady=1)
        
        self.label_lb= ctk.CTkLabel(self.main_panel,text='Borrowing limit')
        self.label_lb.grid(row=4, column=0, sticky="w", padx=1, pady=1)
        self.entry_lb = ctk.CTkEntry(self.main_panel,placeholder_text="Amout of books a user can simultaneously borrow ")
        self.entry_lb.grid(row=4, column=1, sticky="ew", pady=1)
        
        self.label_bpws= ctk.CTkLabel(self.main_panel,text='Borrow price with subscription')
        self.label_bpws.grid(row=5, column=0, sticky="w", padx=1, pady=1)
        self.entry_bpws = ctk.CTkEntry(self.main_panel,placeholder_text="€")
        self.entry_bpws.grid(row=5, column=1, sticky="ew", pady=1)
        
        self.label_bpwts= ctk.CTkLabel(self.main_panel,text='Borrow price without subscription')
        self.label_bpwts.grid(row=6, column=0, sticky="w", padx=1, pady=1)
        self.entry_bpwts = ctk.CTkEntry(self.main_panel,placeholder_text="€")
        self.entry_bpwts.grid(row=6, column=1, sticky="ew", pady=1)
        
        self.label_bd= ctk.CTkLabel(self.main_panel,text='Maximum borrow time')
        self.label_bd.grid(row=7, column=0, sticky="w", padx=1, pady=1)
        self.entry_bd = ctk.CTkEntry(self.main_panel,placeholder_text="Maximum amout of time a user can borrow a book (In days)")
        self.entry_bd.grid(row=7, column=1, sticky="ew", pady=1)
        
        self.label_lr= ctk.CTkLabel(self.main_panel,text='Max book reservation')
        self.label_lr.grid(row=9, column=0, sticky="w", padx=1, pady=1)
        self.entry_lr = ctk.CTkEntry(self.main_panel,placeholder_text="Maximum amout of books a user can add to a reservation")
        self.entry_lr.grid(row=9, column=1, sticky="ew", pady=1)

        self.entry_name.insert(0, library.name)
        self.entry_fpd.insert(0, str(library.fine_per_day))
        self.entry_sa.insert(0, str(library.subscribe_amout))
        self.entry_lb.insert(0, str(library.limit_borrow))
        self.entry_bpws.insert(0, str(library.borrow_price_with_sub))
        self.entry_bpwts.insert(0, str(library.borrow_price_without_sub))
        self.entry_bd.insert(0, str(library.borrow_delay))
        self.entry_lr.insert(0, str(library.limit_reservation))

        self.save_button = ctk.CTkButton(self.main_panel, text="Save", command=self.update_libraries)
        self.save_button.grid(row=10, column=0, columnspan=2, pady=10)
    def update_libraries(self):
        """
        Updates the library parameters from the form values and calls the update_library method on the library service
        with the updated parameters.
        
        """

        try:
            id=self.paramlib[0].id
            name = self.entry_name.get()
            fine_per_day = float(self.entry_fpd.get())
            subscribe_amount = float(self.entry_sa.get())
            limit_borrow = int(self.entry_lb.get())
            borrow_with_sub = float(self.entry_bpws.get())
            borrow_without_sub = float(self.entry_bpwts.get())
            borrow_delay = int(self.entry_bd.get())
            limit_reservation = int(self.entry_lr.get())

            updatelib=self.library_service.update_library(id,name,fine_per_day,subscribe_amount,limit_borrow,borrow_with_sub,borrow_without_sub,borrow_delay,limit_reservation)
            if isinstance(updatelib, str):
                PopUpMessage.pop_up(self, updatelib)
            else:
                PopUpMessage.pop_up(self, "Library added successfully!")
                self.destroy()
                
        except ValueError as e:
            PopUpMessage.pop_up(self, f"Input error: {e}")
        
    def add_form(self):
        
        
        """
        Creates the form to add a new library.
        """
        self.label_name= ctk.CTkLabel(self.main_panel,text='Name')
        self.label_name.grid(row=1, column=0, sticky="w", padx=1, pady=1)
        self.entry_name = ctk.CTkEntry(self.main_panel,placeholder_text="Name of the library")
        self.entry_name.grid(row=1, column=1, sticky="ew", pady=1)
        
        self.label_fpd= ctk.CTkLabel(self.main_panel,text='Daily overdue fee')
        self.label_fpd.grid(row=2, column=0, sticky="w", padx=1, pady=1)
        self.entry_fpd = ctk.CTkEntry(self.main_panel,placeholder_text="Amout (in €) a user will be fined per day if a book is late to be returned")
        self.entry_fpd.grid(row=2, column=1, sticky="ew", pady=1)
        
        self.label_sa= ctk.CTkLabel(self.main_panel,text='Subscription price')
        self.label_sa.grid(row=3, column=0, sticky="w", padx=1, pady=1)
        self.entry_sa = ctk.CTkEntry(self.main_panel,placeholder_text="€")
        self.entry_sa.grid(row=3, column=1, sticky="ew", pady=1)
        
        self.label_lb= ctk.CTkLabel(self.main_panel,text='Borrowing limit')
        self.label_lb.grid(row=4, column=0, sticky="w", padx=1, pady=1)
        self.entry_lb = ctk.CTkEntry(self.main_panel,placeholder_text="Amout of books a user can simultaneously borrow ")
        self.entry_lb.grid(row=4, column=1, sticky="ew", pady=1)
        
        self.label_bpws= ctk.CTkLabel(self.main_panel,text='Borrow price with subscription')
        self.label_bpws.grid(row=5, column=0, sticky="w", padx=1, pady=1)
        self.entry_bpws = ctk.CTkEntry(self.main_panel,placeholder_text="€")
        self.entry_bpws.grid(row=5, column=1, sticky="ew", pady=1)
        
        self.label_bpwts= ctk.CTkLabel(self.main_panel,text='Borrow price without subscription')
        self.label_bpwts.grid(row=6, column=0, sticky="w", padx=1, pady=1)
        self.entry_bpwts = ctk.CTkEntry(self.main_panel,placeholder_text="€")
        self.entry_bpwts.grid(row=6, column=1, sticky="ew", pady=1)
        
        self.label_bd= ctk.CTkLabel(self.main_panel,text='Maximum borrow time')
        self.label_bd.grid(row=7, column=0, sticky="w", padx=1, pady=1)
        self.entry_bd = ctk.CTkEntry(self.main_panel,placeholder_text="Maximum amout of time a user can borrow a book (In days)")
        self.entry_bd.grid(row=7, column=1, sticky="ew", pady=1)
        
        self.label_lr= ctk.CTkLabel(self.main_panel,text='Max book reservation')
        self.label_lr.grid(row=9, column=0, sticky="w", padx=1, pady=1)
        self.entry_lr = ctk.CTkEntry(self.main_panel,placeholder_text="Maximum amout of books a user can add to a reservation")
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


