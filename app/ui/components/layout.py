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
