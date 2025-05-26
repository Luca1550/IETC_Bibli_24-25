import customtkinter as ctk
from ui import BOOKS
from ui.components import MenuNavigation, LoginPage

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BIBLIOTHEQUE")
        self.geometry("1600x900")

        self.grid_rowconfigure(1, weight=1)  
        self.grid_columnconfigure(0, weight=1)

        # Crée une frame qui prend tout l'écran
        self.login_container = ctk.CTkFrame(self)
        self.login_container.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # Crée une sous-frame dans login_container pour centrer LoginPage
        self.center_frame = ctk.CTkFrame(self.login_container)
        self.center_frame.pack(expand=True)

        # LoginPage centré à l'intérieur
        self.login_frame = LoginPage(self.center_frame, on_login=self.login_success)
        self.login_frame.pack(padx=40, pady=40)

        self.menu = None
        self.page_container = None
        self.current_page = None
        
    def login_success(self):
        self.login_frame.destroy()

        # Affiche le menu et la zone de page
        self.menu = MenuNavigation(self, on_menu_select=self.change_page)
        self.menu.grid(row=0, column=0, sticky="ew")

        self.page_container = ctk.CTkFrame(self)
        self.page_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.change_page("home")


    def change_page(self, page_name):
        if self.current_page:
            self.current_page.destroy()

        def home():
            display = BOOKS()
            return ctk.CTkLabel(self.page_container, text=display.display_books())

        def page1():
            return ctk.CTkLabel(self.page_container, text="Contenu de la Page 1")

        def page2():
            return ctk.CTkLabel(self.page_container, text="Contenu de la Page 2")

        page_switch = {
            "home": home,
            "page1": page1,
            "page2": page2,
        }

        # Appelle la fonction correspondant à la page, ou affiche une page vide si inconnue
        self.current_page = page_switch.get(page_name, lambda: ctk.CTkLabel(self.page_container, text="Page inconnue"))()
        self.current_page.pack(expand=True)
 
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = MainApp()
    app.mainloop()
