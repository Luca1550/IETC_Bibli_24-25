import customtkinter as ctk
from services import LibraryService
from ui.components import MenuNavigation, LoginPage
from ui.pages import BookPage,LibraryPage
from ui.pages.library import LibraryPage
from ui.pages.book import BookPage
from ui.pages.reservation import ReservationPage
from ui.pages.library import LibraryPage
from ui.pages.worker import WorkerPage
from ui.pages.borrow import BorrowPage
from ui.pages.member import MemberPage

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
        self.title("")
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
        self.library_service = LibraryService()
        self.paramlib = self.library_service.get_library_parameters()

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

        
        if len(self.paramlib) ==0:
            self.change_page("Config")

        else:    
            self.change_page("Home")


    def change_page(self, page_name):
        """
        Changes the current page displayed in the page container.
        :param page_name: The name of the page to display.
        """
        if self.current_page:
            self.current_page.destroy()

        def home_page():
            return ctk.CTkLabel(self.page_container, text="Welcome in the Library")

        def book_page():
            return BookPage(self.page_container)

        def reservation_page():
            return ReservationPage(self.page_container)

        def borrow_page():
            return BorrowPage(self.page_container)

        def members_page():
            return MemberPage(self.page_container)

        def config_page():
            return LibraryPage(self.page_container)

        def worker_page():
            return WorkerPage(self.page_container)

        page_switch = {
            "Home": home_page,
            "Books": book_page,
            "Reservation": reservation_page,
            "Borrow":borrow_page,
            "Members":members_page,
            "Config":config_page,
            "Workers":worker_page
        }

        self.current_page = page_switch.get(page_name, lambda: ctk.CTkLabel(self.page_container, text="Unknown Page"))()
        self.current_page.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = MainApp()
    app.mainloop()
