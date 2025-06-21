
import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from services import ReservationService,BookService,ExemplarService,MemberService,PersonService
from ui.components import PopUpMessage,SelectionFrame
from datetime import date 
from datetime import datetime

#ok donc a gauche on va pouvoir voir les reservations et qu'elles soient clickable 
#a droite on peut faire une reservation et quand on clique sur une reservation on a le bouton update a la place de add 
#verifier pour le changement de statut 


class ReservationPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.reservation_service = ReservationService()
        self.book_service = BookService()
        self.exemplar_service = ExemplarService()
        self.member_service = MemberService()
        self.personne_servce= PersonService()
        self.selected_reservation= None
        self.setup_ui()
        self.book_selected =[]
        self.member_selected=[]
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

            #ici je vais du coup rajouter les autres infos de livre etc pour la listbox
            member_firstname=self.personne_servce.get_by_id(res.member.id_person).first_name if res.member else "Inconnu"
            member_name=self.personne_servce.get_by_id(res.member.id_person).last_name if res.member else "Inconnu"
            self.reservation_listbox.insert("end", f"{res.reservation_date} | Ex: {res.id_exemplar} | Membre: {member_firstname} {member_name}")
            self.indexbook[idx] = res
        self.reservation_listbox.bind("<<ListboxSelect>>", self.reservation_select)

        self.right_panel = ctk.CTkFrame(self.main_panel)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        self.form_title = ctk.CTkLabel(self.right_panel, text="New Réservation", font=ctk.CTkFont(size=18, weight="bold"))
        self.form_title.pack(pady=(10, 10))
        self.title_entry = ctk.CTkEntry(self.right_panel, placeholder_text="title")
        self.title_entry.pack(pady=5, padx=20, fill="x")
        self.all_books= []
        for book in self.book_service.get_all():
            exemplars = self.exemplar_service.get_all_by_isbn(book.isbn)
            for exemplar in exemplars:
                if exemplar.status.value != 3 :
                    self.all_books.append(book)
                    break
        self.edit_book_button = ctk.CTkButton(self.right_panel, text="✏️", width=30, command=lambda:self.open_selection_frame(
            title="Book",
            all_items=self.all_books,
            selected_items=self.book_selected,
            display_model_method=lambda book: f"{book.title}",
            attributes_to_search=[lambda book: {book.title}],
            entry_to_update=self.title_entry
        ))
        self.member_entry = ctk.CTkEntry(self.right_panel, placeholder_text="Member")
        self.member_entry.pack(pady=5, padx=20, fill="x")
        self.edit_member_button = ctk.CTkButton(self.right_panel, text="✏️", width=30, command=lambda:self.open_selection_frame(
            title="Member",
            all_items=self.member_service.get_all_members(),
            selected_items=self.member_selected,
            display_model_method=lambda member: f"{member.person.first_name}",
            attributes_to_search=[lambda member: {member.person.first_name}],
            entry_to_update=self.member_entry
        ))
        self.date_entry = ctk.CTkEntry(self.right_panel, placeholder_text="Date (YYYY-MM-DD)")
        self.date_entry.pack(pady=5, padx=20, fill="x")

        self.edit_book_button.pack(pady=(10, 10))
        self.edit_member_button.pack(pady=(10, 10))
        
        self.submit_button = ctk.CTkButton(self.right_panel, text="Réserver",command=self.add_reservation)
        self.submit_button.pack(pady=20)
    def add_reservation(self):
        try:
            if len(self.member_selected) ==1:
                id_member= self.member_selected[0].id_member
            else:
                PopUpMessage.pop_up(self, "More than one exemplar")
                return 

            if len(self.book_selected) ==1:
                id_exemplar= self.exemplar_service.get_all_by_isbn(self.book_selected[0])
            else:
                PopUpMessage.pop_up(self, "More than one exemplar")
                return 
            if id_exemplar is None:
                PopUpMessage.pop_up(self, "Exemplar not found for the given title.")
                return
            if datetime.fromisoformat(self.date_entry.get()) > datetime.fromisoformat(date.today().isoformat()):
                reservation_date = str(self.date_entry.get())
            else:
                PopUpMessage.pop_up(self, "Wrong date")
                return
            newreservation=self.reservation_service.add_reservation(self.book_selected[0].isbn,id_member,reservation_date)
            if isinstance(newreservation, str):
                PopUpMessage.pop_up(self, newreservation)
            else:
                PopUpMessage.pop_up(self, "reservation added successfully!")
                self.destroy()

        except ValueError as e:
            PopUpMessage.pop_up(self, f"Input error: {e}")

    def update_reservation(self):
        try:
            id_reservation = int(self.reservation_entry.get())
            id_exemplar = int(self.name_entry.get())
            if len(self.member_selected) ==1:
                id_member= self.member_selected[0].id_member
            else:
                PopUpMessage.pop_up(self, "More than one member")
                return 
            reservation_date = str(self.date_entry.get())
            newreservation=self.reservation_service.update_reservation(id_reservation,id_exemplar,id_member,reservation_date)
            if isinstance(newreservation, str):
                PopUpMessage.pop_up(self, newreservation)
            else:
                PopUpMessage.pop_up(self, "reservation updated successfully!")
                self.destroy()
        except ValueError as e:
            PopUpMessage.pop_up(self, f"Input error: {e}")
        self.destroy()

    
    def reservation_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_res = self.indexbook.get(index)
            self.title_entry.delete(0, tk.END)
            self.member_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.book_selected.clear()
            self.member_selected.clear()
            self.title_entry.destroy()
            self.member_entry.destroy()
            self.date_entry.destroy()
            self.edit_book_button.destroy()
            self.edit_member_button.destroy()
            self.form_title.destroy()


            self.form_title = ctk.CTkLabel(self.right_panel, text="Update Reservation", font=ctk.CTkFont(size=18, weight="bold"))
            self.form_title.pack(pady=(10, 10))
            self.reservation_entry = ctk.CTkEntry(self.right_panel, placeholder_text="id_reservation")
            self.reservation_entry.pack(pady=5, padx=20, fill="x")
            self.member_entry = ctk.CTkEntry(self.right_panel, placeholder_text="Member")
            self.member_entry.pack(pady=5, padx=20, fill="x")
            
            self.name_entry = ctk.CTkEntry(self.right_panel, placeholder_text="id_exemplar")
            self.name_entry.pack(pady=5, padx=20, fill="x")
            self.member_entry = ctk.CTkEntry(self.right_panel, placeholder_text="id_member")
            self.member_entry.pack(pady=5, padx=20, fill="x")
            self.date_entry = ctk.CTkEntry(self.right_panel, placeholder_text="reservation_date")
            self.date_entry.pack(pady=5, padx=20, fill="x")
            self.submit_button.destroy() 

            self.submit_button = ctk.CTkButton(self.right_panel, text="Update", command=self.update_reservation)
            self.submit_button.pack(pady=20)
            if selected_res:
                self.selected_reservation = selected_res
                print("MEMMMM",self.personne_servce.get_by_id(selected_res.member.id_person).first_name )
                self.member_selected.append(selected_res.member)
                for key, value in vars(self.selected_reservation).items():
                    print(f"{key}: {value}")
                    # if key == "member":
                    #     self.member_selected.append(value)
                        # for truc in value:

                self.edit_member_button = ctk.CTkButton(self.right_panel, text="✏️", width=30, command=lambda:self.open_selection_frame(
                title="Member",
                all_items=self.member_service.get_all_members(),
                selected_items=self.member_selected,
                #demander à JULIEN mais pq ma liste est vide sinon tout ok 
                display_model_method=lambda member: f"{self.personne_servce.get_by_id(member.id_person).first_name}",
                attributes_to_search=[lambda member: {member.person.first_name}],
                entry_to_update=self.member_entry
                ))
                self.edit_member_button.pack(pady=(10, 10))
                    # self.reservation_entry.insert(0, selected_res.id_reservation)
                    # self.name_entry.insert(0, selected_res.id_exemplar)
                    # self.member_entry.insert(0, selected_res.)
                    # self.date_entry.insert(0, selected_res.reservation_date)
                
                
        
    def open_selection_frame(self,title,all_items,selected_items,display_model_method,attributes_to_search,entry_to_update,attributes_to_entry=None):
        """
            opens a selection frame to choose items from a list.
        """
        selection_frame = SelectionFrame(
            self,
            title,
            all_items,
            selected_items,
            display_model_method,
            attributes_to_search,
            entry_to_update,
            attributes_to_entry
        )
        self.wait_window(selection_frame)