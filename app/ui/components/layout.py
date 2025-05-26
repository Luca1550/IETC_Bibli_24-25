import customtkinter as ctk

class MenuNavigation(ctk.CTkFrame):
    def __init__(self, parent, on_menu_select, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.on_menu_select = on_menu_select
        self.current_active = None

        self.default_color = "#2b2da3"   # Couleur normale des boutons
        self.active_color = "#2d47da"    # Rose
        self.hover_color = "#2d47da"     # Rose clair

        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_home = ctk.CTkButton(self, text="Accueil", command=lambda: self.select_page("home"))
        self.btn_page1 = ctk.CTkButton(self, text="Page 1", command=lambda: self.select_page("page1"))
        self.btn_page2 = ctk.CTkButton(self, text="Page 2", command=lambda: self.select_page("page2"))

        self.buttons = {
            "home": self.btn_home,
            "page1": self.btn_page1,
            "page2": self.btn_page2
        }

        for idx, btn in enumerate(self.buttons.values()):
            btn.configure(
                fg_color=self.default_color,
                hover_color=self.hover_color,
                text_color="white"
            )
            btn.grid(row=0, column=idx, padx=10, pady=10, sticky="ew")

    def select_page(self, page_name):
        self.set_active_button(page_name)
        self.on_menu_select(page_name)

    def set_active_button(self, active_key):
        for key, btn in self.buttons.items():
            if key == active_key:
                btn.configure(fg_color=self.active_color)
                self.current_active = btn
            else:
                btn.configure(fg_color=self.default_color)

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, on_login, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.on_login = on_login  # callback après connexion réussie

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Connexion", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=(20, 10))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nom d'utilisateur")
        self.username_entry.grid(row=1, column=0, padx=40, pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Mot de passe", show="*")
        self.password_entry.grid(row=2, column=0, padx=40, pady=10)

        self.login_button = ctk.CTkButton(self, text="Se connecter", command=self.attempt_login)
        self.login_button.grid(row=3, column=0, padx=40, pady=20)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=4, column=0)

    def attempt_login(self):
        userTest = "admin"
        passwordTest = "admin"

        username = self.username_entry.get()
        password = self.password_entry.get()

        # Exemple simple : login = admin, mdp = 1234
        if username == userTest and password == passwordTest :
            self.error_label.configure(text="")
            self.on_login()  # Appel du callback
        else:
            self.error_label.configure(text="Identifiants incorrects")