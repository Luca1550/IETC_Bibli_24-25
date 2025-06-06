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
        self.btn_page_Accueil = ctk.CTkButton(self, text="Accueil", command=lambda: self.select_page("Accueil"))
        self.btn_page_Livres = ctk.CTkButton(self, text="Livres", command=lambda: self.select_page("Livres"))
        self.btn_page_Réservation = ctk.CTkButton(self, text="Réservation", command=lambda: self.select_page("Réservation"))
        self.btn_page_Emprunt = ctk.CTkButton(self, text="Emprunt", command=lambda: self.select_page("Emprunt"))
        self.btn_page_Membres = ctk.CTkButton(self, text="Membres", command=lambda: self.select_page("Membres"))
        self.btn_page_Employes = ctk.CTkButton(self, text="Employes", command=lambda: self.select_page("Employes"))
        self.btn_page_Config = ctk.CTkButton(self, text="Config", command=lambda: self.select_page("Config"))
        

        self.buttons = {
            "Accueil": self.btn_page_Accueil,
            "Livres": self.btn_page_Livres,
            "Réservation": self.btn_page_Réservation,
            "Emprunt": self.btn_page_Emprunt,
            "Membres": self.btn_page_Membres
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
        
        self.btn_page_Employes.configure(
            fg_color="#dd5019",
            hover_color="#cf714c",
            text_color="white",
            width=120,
            height=50,
        )
        self.btn_page_Employes.grid(row=0, column=8, pady=20, sticky="e")

        self.btn_page_Config.configure(
            fg_color="#dd5019",
            hover_color="#cf714c",
            text_color="white",
            width=120,
            height=50,
        )
        self.btn_page_Config.grid(row=0, column=9, padx=10, pady=20, sticky="s")

        

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

        ctk.CTkLabel(self, text="Connexion", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=(20, 10))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nom d'utilisateur")
        self.username_entry.grid(row=1, column=0, padx=40, pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Mot de passe", show="*")
        self.password_entry.grid(row=2, column=0, padx=40, pady=10)

        self.login_button = ctk.CTkButton(self, text="Se connecter", command=self.check_connexion)
        self.login_button.grid(row=3, column=0, padx=40, pady=20)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=4, column=0)

    def check_connexion(self):
        """
        Checks the entered username and password against predefined credentials.
        If the credentials match, it calls the `on_login` callback; otherwise, it displays an error message.
        """
        # Predefined credentials for testing
        userTest = ""
        passwordTest = ""

        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == userTest and password == passwordTest :
            self.error_label.configure(text="")
            self.on_login()  
        else:
            self.error_label.configure(text="Identifiants incorrects")