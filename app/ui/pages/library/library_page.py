
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
        Displays the title "Bibliothèque" at the top of the form.

        Depending on the number of library parameters retrieved, either
        initializes the form for updating library parameters or adding a new library.
        Displays an error message if more than one library is found.
        """

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  

        # le truc sticky nsew est globalement pour dire que la page s'etire dans toutes la grille du nord ouest,.... 
        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        

        self.form_title = ctk.CTkLabel(self.main_panel, text="Bibliothèque", font=ctk.CTkFont(size=18, weight="bold"))
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
        self.labelName= ctk.CTkLabel(self.main_panel,text='Name')
        self.labelName.grid(row=1, column=0, sticky="w", padx=1, pady=1)
        self.nameentry = ctk.CTkEntry(self.main_panel)
        self.nameentry.grid(row=1, column=1, sticky="ew", pady=1)
        self.labelFPD= ctk.CTkLabel(self.main_panel,text='Fine per day')
        self.labelFPD.grid(row=2, column=0, sticky="w", padx=1, pady=1)
        self.FPDentry = ctk.CTkEntry(self.main_panel)
        self.FPDentry.grid(row=2, column=1, sticky="ew", pady=1)
        self.labelSA= ctk.CTkLabel(self.main_panel,text='Subscribe amount')
        self.labelSA.grid(row=3, column=0, sticky="w", padx=1, pady=1)
        self.SAentry = ctk.CTkEntry(self.main_panel)
        self.SAentry.grid(row=3, column=1, sticky="ew", pady=1)
        self.labelLB= ctk.CTkLabel(self.main_panel,text='Limit borrow')
        self.labelLB.grid(row=4, column=0, sticky="w", padx=1, pady=1)
        self.LBentry = ctk.CTkEntry(self.main_panel)
        self.LBentry.grid(row=4, column=1, sticky="ew", pady=1)
        self.labelBPWS= ctk.CTkLabel(self.main_panel,text='Borrow price with sub')
        self.labelBPWS.grid(row=5, column=0, sticky="w", padx=1, pady=1)
        self.BPWSentry = ctk.CTkEntry(self.main_panel)
        self.BPWSentry.grid(row=5, column=1, sticky="ew", pady=1)
        self.labelBPWTS= ctk.CTkLabel(self.main_panel,text='Borrow price without sub')
        self.labelBPWTS.grid(row=6, column=0, sticky="w", padx=1, pady=1)
        self.BPWTSentry = ctk.CTkEntry(self.main_panel)
        self.BPWTSentry.grid(row=6, column=1, sticky="ew", pady=1)
        self.labelBD= ctk.CTkLabel(self.main_panel,text='Borrow delay')
        self.labelBD.grid(row=7, column=0, sticky="w", padx=1, pady=1)
        self.BDentry = ctk.CTkEntry(self.main_panel)
        self.BDentry.grid(row=7, column=1, sticky="ew", pady=1)
        self.labelUrl= ctk.CTkLabel(self.main_panel,text='Url logo')
        self.labelUrl.grid(row=8, column=0, sticky="w", padx=1, pady=1)
        self.urlentry = ctk.CTkEntry(self.main_panel)
        self.urlentry.grid(row=8, column=1, sticky="ew", pady=1)
        self.labelLR= ctk.CTkLabel(self.main_panel,text='Limit reservation')
        self.labelLR.grid(row=9, column=0, sticky="w", padx=1, pady=1)
        self.LRentry = ctk.CTkEntry(self.main_panel)
        self.LRentry.grid(row=9, column=1, sticky="ew", pady=1)

        self.add_button = ctk.CTkButton(self.main_panel, text="Add",command=self.add_library)
        self.add_button.grid(row=10, column=0, columnspan=2, pady=10)

    def add_library(self):
        """
        Collects input values from the form fields and attempts to add a new library using the LibraryService.
        
        Retrieves the name, fine per day, subscription amount, limit on borrowable items,
        borrowing price with and without subscription, borrowing delay, and URL for the library logo
        from user input. Converts the numerical values to the appropriate types.
        
        Calls the add_library method of the LibraryService with the collected parameters.
        Displays a success pop-up message if the library is added successfully.
        If any input errors occur, a pop-up message is displayed with the error details.
        """

        try:
            name = self.nameentry.get()
            fine_per_day = float(self.FPDentry.get())
            subscribe_amount = float(self.SAentry.get())
            limit_borrow = int(self.LBentry.get())
            borrow_with_sub = float(self.BPWSentry.get())
            borrow_without_sub = float(self.BPWTSentry.get())
            borrow_delay = int(self.BDentry.get())
            url_logo = self.urlentry.get()
            limit_reservation = int(self.LRentry.get())
            newlib=self.library_service.add_library(name,fine_per_day,subscribe_amount,limit_borrow,borrow_with_sub,borrow_without_sub,borrow_delay,url_logo,limit_reservation)
            if isinstance(newlib, str):
                PopUpMessage.pop_up(self, newlib)
            else:
                PopUpMessage.pop_up(self, "Library added successfully!")
                self.destroy()
                
        except ValueError as e:
            PopUpMessage.pop_up(self, f"Input error: {e}")


