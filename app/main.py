import customtkinter as ctk
from ui.components import MenuNavigation, LoginPage
from ui.pages.library import LibraryPage
class MainApp(ctk.CTk):
    """
    Main application class that initializes the main window and handles login and page navigation.
    It contains a login frame that transitions to a menu and page container upon successful login.
    """
    def __init__(self):
        """
        Initializes the MainApp class, sets up the main window, and creates the login frame.
        """
        super().__init__()
        self.title("BIBLIOTHEQUE")
        self.geometry("1280x720")

        self.grid_rowconfigure(1, weight=1)  
        self.grid_columnconfigure(0, weight=1)

        self.login_container = ctk.CTkFrame(self)
        self.login_container.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.center_frame = ctk.CTkFrame(self.login_container)
        self.center_frame.pack(expand=True)

        self.login_frame = LoginPage(self.center_frame, on_login=self.login_success)
        self.login_frame.pack(padx=40, pady=40)

        self.menu = None
        self.page_container = None
        self.current_page = None
        
    def login_success(self):
        """
        Callback function that is called when the user successfully logs in.
        It destroys the login frame and initializes the menu and page container.
        """
        self.login_frame.destroy()

        self.menu = MenuNavigation(self, on_menu_select=self.change_page,)
        self.menu.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.page_container = ctk.CTkFrame(self)
        self.page_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.page_container.grid_rowconfigure(0, weight=1)
        self.page_container.grid_columnconfigure(0, weight=1)

        self.change_page("Accueil")


    def change_page(self, page_name):
        """
        Changes the current page displayed in the page container.
        :param page_name: The name of the page to display.
        """
        if self.current_page:
            self.current_page.destroy()

        def page_Accueil():
            return ctk.CTkLabel(self.page_container, text="Bienvenue dans la Bibliothèque")

        def page_Livres():
            return ctk.CTkLabel(self.page_container, text="Contenu de la Page Livres")

        def page_Réservation():
            return ctk.CTkLabel(self.page_container, text="Contenu de la Page Réservation")

        def page_Emprunt():
            return ctk.CTkLabel(self.page_container, text="Contenu de la Page Emprunt")

        def page_Membres():
            return ctk.CTkLabel(self.page_container, text="Contenu de la Page Membres")

        def page_Config():
            return LibraryPage(self.page_container)

        def page_Employes():
            return ctk.CTkLabel(self.page_container, text="Contenu de la Page Employes")

        page_switch = {
            "Accueil": page_Accueil,
            "Livres": page_Livres,
            "Réservation": page_Réservation,
            "Emprunt":page_Emprunt,
            "Membres":page_Membres,
            "Config":page_Config,
            "Employes":page_Employes
        }

        
        self.current_page = page_switch.get(page_name, lambda: ctk.CTkLabel(self.page_container, text="Page inconnue"))()
        self.current_page.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = MainApp()
    app.mainloop()
