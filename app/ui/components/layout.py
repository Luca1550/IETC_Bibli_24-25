import customtkinter as ctk

class MenuNavigation(ctk.CTkFrame):
    """
    A navigation menu for switching between different pages in the application.
    It contains buttons for Home, Page 1, Page 2, and Page 3.
    When a button is clicked, it calls the `on_menu_select` callback with the name of the page.
    """
    def __init__(self, parent, on_menu_select, *args, **kwargs):
        """
        Initializes the MenuNavigation frame.
        :param parent: The parent widget to which this frame will be attached.
        :param on_menu_select: A callback function that is called when a menu item is selected.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(parent, *args, **kwargs)

        self.on_menu_select = on_menu_select
        self.current_active = None

        self.default_color = "#2b2da3"   
        self.active_color = "#2d47da"    
        self.hover_color = "#2d47da"     

        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(border_width=1, corner_radius=10, bg_color="transparent", fg_color="transparent")
        self.create_buttons()

    def create_buttons(self):
        """
        Creates the navigation buttons for the menu.
        """
        self.btn_home_page = ctk.CTkButton(self, text="Home", command=lambda: self.select_page("Home"))
        self.master.bind_all("<F1>", lambda event: self.btn_home_page.invoke())
        self.btn_book_page = ctk.CTkButton(self, text="Books", command=lambda: self.select_page("Books"))
        self.master.bind_all("<F2>", lambda event: self.btn_book_page.invoke())
        self.btn_reservation_page = ctk.CTkButton(self, text="Reservation", command=lambda: self.select_page("Reservation"))
        self.master.bind_all("<F3>", lambda event: self.btn_reservation_page.invoke())
        self.btn_borrow_page = ctk.CTkButton(self, text="Borrow", command=lambda: self.select_page("Borrow"))
        self.master.bind_all("<F4>", lambda event: self.btn_borrow_page.invoke())
        self.btn_members_page = ctk.CTkButton(self, text="Members", command=lambda: self.select_page("Members"))
        self.master.bind_all("<F5>", lambda event: self.btn_members_page.invoke())
        self.btn_workers_page = ctk.CTkButton(self, text="Workers", command=lambda: self.select_page("Workers"))
        self.master.bind_all("<F6>", lambda event: self.btn_workers_page.invoke())
        self.btn_config_page = ctk.CTkButton(self, text="Config", command=lambda: self.select_page("Config"))
        self.master.bind_all("<F7>", lambda event: self.btn_config_page.invoke())
        

        self.buttons = {
            "Home": self.btn_home_page,
            "Books": self.btn_book_page,
            "Reservation": self.btn_reservation_page,
            "Borrow": self.btn_borrow_page,
            "Members": self.btn_members_page,
        }

        
        for idx, btn in enumerate(self.buttons.values()):
            btn.configure(
                fg_color=self.default_color,
                hover_color=self.hover_color,
                text_color="white",
                width=120,
                height=50,
            )
            btn.grid(row=0, column=idx, padx=10, pady=20, sticky="ew")

        self.btn_workers_page.configure(
            fg_color="#dd5019",
            hover_color="#cf714c",
            text_color="white",
            width=120,
            height=50,
        )
        self.btn_workers_page.grid(row=0, column=8, pady=20, sticky="e")

        self.btn_config_page.configure(
            fg_color="#dd5019",
            hover_color="#cf714c",
            text_color="white",
            width=120,
            height=50,
        )
        self.btn_config_page.grid(row=0, column=9, padx=10, pady=20, sticky="s")

        

        for i in range(10):
            if i in [5, 6 ,7 ,8]:
                self.grid_columnconfigure(i, weight=5)  
            else:
                self.grid_columnconfigure(i, weight=1)

    def select_page(self, page_name):
        """
        Selects a page and updates the active button.
        """
        self.set_active_button(page_name)
        self.on_menu_select(page_name)
    
    def set_active_button(self, active_key):
        """
        Sets the active button based on the provided key.
        :param active_key: The key of the button to set as active.
        """
        for key, btn in self.buttons.items():
            if key == active_key:
                btn.configure(fg_color=self.active_color)
                self.current_active = btn
            else:
                btn.configure(fg_color=self.default_color)

class LoginPage(ctk.CTkFrame):
    """
    A login page that allows users to enter their username and password.
    When the user clicks the login button, it checks the credentials and calls the `on_login` callback if successful.
    """
    def __init__(self, parent, on_login, *args, **kwargs):
        """
        Initializes the LoginPage frame.
        :param parent: The parent widget to which this frame will be attached.
        :param on_login: A callback function that is called when the login is successful.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(parent, *args, **kwargs)

        self.on_login = on_login  

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Login", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=(20, 10))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.grid(row=1, column=0, padx=40, pady=10)
        self.username_entry.focus_set()
        self.username_entry.bind("<Return>", lambda event: self.login_button.invoke())

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.grid(row=2, column=0, padx=40, pady=10)
        self.password_entry.bind("<Return>", lambda event: self.login_button.invoke())

        self.login_button = ctk.CTkButton(self, text="Login", command=self.check_connexion)
        self.login_button.grid(row=3, column=0, padx=40, pady=20)
        self.bind("<Return>", lambda event: self.login_button.invoke())

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=4, column=0)

    def check_connexion(self):
        """
        Checks the entered username and password against predefined credentials.
        If the credentials match, it calls the `on_login` callback; otherwise, it displays an error message.
        """
        # Predefined credentials for testing
        userStandart = ""
        passwordStandart = ""

        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == userStandart and password == passwordStandart:
            self.error_label.configure(text="")
            self.on_login()  
        else:
            self.error_label.configure(text="Incorrect Credentials")