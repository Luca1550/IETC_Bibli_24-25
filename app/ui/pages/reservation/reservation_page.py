
import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from services import ReservationService,BookService,ExemplarService
from ui.components import PopUpMessage

#ok donc a gauche on va pouvoir voir les reservations et qu'elles soient clickable 
#a droite on peut faire une reservation et quand on clique sur une reservation on a le bouton update a la place de add 
#verifier pour le changement de statut 


class ReservationPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.reservation_service = ReservationService()
        self.book_service = BookService()
        self.exemplar_service = ExemplarService()
        self.selected_reservation= None
        self.setup_ui()
        
    def setup_ui(self):
        

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  

        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        

        self.form_title = ctk.CTkLabel(self.main_panel, text="Rerservation", font=ctk.CTkFont(size=18, weight="bold"))
        self.form_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self.paramres = self.reservation_service.get_all()

        
        self.main_panel.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Configu 2 col
        self.main_panel.grid_columnconfigure(0, weight=1)
        self.main_panel.grid_columnconfigure(1, weight=2)
        self.main_panel.grid_rowconfigure(0, weight=1)

        self.left_panel = ctk.CTkFrame(self.main_panel)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.left_label = ctk.CTkLabel(self.left_panel, text="Mes Réservations", font=ctk.CTkFont(size=16, weight="bold"))
        self.left_label.pack(pady=(10, 5))

        self.reservation_listbox = tk.Listbox(self.left_panel,  height=40)
        self.reservation_listbox.pack(expand=True, fill="both", padx=10, pady=10)

        self.paramres = self.reservation_service.get_all()
        self.indexbook = {}
        for idx,res in enumerate(self.paramres):
            #ici je vais du coup rajouter les autres infos de livre etc 
            self.reservation_listbox.insert("end", f"{res.id_exemplar} - {res.reservation_date}\n")
            self.indexbook[idx] = res 
        self.reservation_listbox.bind("<<ListboxSelect>>", self.reservation_select)

        self.right_panel = ctk.CTkFrame(self.main_panel)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        self.form_title = ctk.CTkLabel(self.right_panel, text="New Réservation", font=ctk.CTkFont(size=18, weight="bold"))
        self.form_title.pack(pady=(10, 10))
        
        self.name_entry = ctk.CTkEntry(self.right_panel, placeholder_text="id_exemplar")
        self.name_entry.pack(pady=5, padx=20, fill="x")
        self.member_entry = ctk.CTkEntry(self.right_panel, placeholder_text="id_member")
        self.member_entry.pack(pady=5, padx=20, fill="x")
        self.date_entry = ctk.CTkEntry(self.right_panel, placeholder_text="Date (YYYY-MM-DD)")
        self.date_entry.pack(pady=5, padx=20, fill="x")
    
        self.submit_button = ctk.CTkButton(self.right_panel, text="Réserver",command=self.add_reservation)
        self.submit_button.pack(pady=20)
    def add_reservation(self):
        try:
            id_exemplar = int(self.name_entry.get())
            id_member = int(self.member_entry.get())
            reservation_date = str(self.date_entry.get())
            newreservation=self.reservation_service.add_reservation(id_exemplar,id_member,reservation_date)
            if isinstance(newreservation, str):
                PopUpMessage.pop_up(self, newreservation)
            else:
                PopUpMessage.pop_up(self, "reservation added successfully!")
                self.destroy()
            self.submit_button.configure(text="Réserver", command=self.add_reservation)

        except ValueError as e:
            PopUpMessage.pop_up(self, f"Input error: {e}")

    def update_reservation(self):
        try:
            id_reservation = int(self.reservation_entry.get())
            id_exemplar = int(self.name_entry.get())
            id_member = int(self.member_entry.get())
            reservation_date = str(self.date_entry.get())
            newreservation=self.reservation_service.update_reservation(id_reservation,id_exemplar,id_member,reservation_date)
            if isinstance(newreservation, str):
                PopUpMessage.pop_up(self, newreservation)
            else:
                PopUpMessage.pop_up(self, "reservation updated successfully!")
                self.destroy()
            self.submit_button.configure(text="Réserver", command=self.add_reservation)
        except ValueError as e:
            PopUpMessage.pop_up(self, f"Input error: {e}")
        self.destroy()

    

    """def spiderManMeme(self):
        #ici je veux qu'on tape le nom du livre et boom 
        #
        # 🕷️   ->  🕷️
        #           ^
        #          /
        #     🕷️



        #En gros on a le nom du livre donc on regarde dans les livres qui a le mm nom et autheur du livre puis si le nom et l'auteur correspondent on a l'isbn
        #avec l'isbn on regarde dans la liste exemplar et la on a son id 
        #On utilise self.book_service.get_all() pour comparer title et author puis on prend l'isbn et dans 
        #
        books = self.book_service.get_all()
        
        i=0
        while i != books[-1]:
            for book in books :
                if book.title == title:
                    book.isbn == isbn
                    id_exemplar = self.exemplar_service.get(id)


"""
    #check apres ca crée un bug 
    def reservation_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_res = self.indexbook.get(index)
            self.reservation_entry = ctk.CTkEntry(self.right_panel, placeholder_text="id_reservation")
            self.reservation_entry.pack(pady=5, padx=20, fill="x")
            if selected_res:
                self.selected_reservation = selected_res

                for key, value in vars(self.selected_reservation).items():
                    print(f"{key}: {value}")

                self.reservation_entry.delete(0, tk.END)
                self.reservation_entry.insert(0, selected_res.id_reservation)

                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, selected_res.id_exemplar)

                self.member_entry.delete(0, tk.END)
                self.member_entry.insert(0, selected_res.id_member)

                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, selected_res.reservation_date)

                self.submit_button.configure(text="Update", command=self.update_reservation)

        
