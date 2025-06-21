import customtkinter as ctk
from tools import Color
class BorrowFrame(ctk.CTkFrame):
    
    
    def __init__(self,parent):
        super().__init__(parent)

        self.main_frame= ctk.CTkFrame(self,fg_color=Color.primary_color(),corner_radius=15)
        self.main_frame.pack(fill="x", padx=5,pady=10)