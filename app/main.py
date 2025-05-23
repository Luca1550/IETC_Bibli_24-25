import customtkinter as ctk
from ui import BOOKS
from ui.components import MenuNavigation

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BIBLIOTHEQUE DE SES GRANDS MORTS")
        self.geometry("1200x800")

        self.grid_rowconfigure(1, weight=1)  
        self.grid_columnconfigure(0, weight=1)

        # Create MENU and call the function when button is pressed
        self.menu = MenuNavigation(self, on_menu_select=self.change_page)
        self.menu.grid(row=0, column=0, sticky="ew")

        # Container to display the pages
        self.page_container = ctk.CTkFrame(self)
        self.page_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.current_page = None
        self.change_page("home")

    def change_page(self, page_name):
        if self.current_page:
            self.current_page.destroy()   
        # insert for each case the method wich displays the page 
        if page_name == "home":
            display = BOOKS()
            self.current_page = ctk.CTkLabel(self.page_container, text=display.display_books())
        elif page_name == "page1":
            self.current_page = ctk.CTkLabel(self.page_container, text="Contenu de la Page 1")
        elif page_name == "page2":
            self.current_page = ctk.CTkLabel(self.page_container, text="Contenu de la Page 2")
        self.current_page.pack(expand=True)
 
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = MainApp()
    app.mainloop()
