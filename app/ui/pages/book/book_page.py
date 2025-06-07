import customtkinter as ctk
import tkinter as tk
from services import BookService
from .book_edit_page import BookEditPage

class BookFrame(ctk.CTkFrame):
    """Frame pour afficher un livre individuel"""
    def __init__(self, parent, book, delete_callback, edit_callback):
        super().__init__(parent)
        
        self.book = book
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        
        self.configure(corner_radius=10, border_width=1)
        self.setup_book_display()
    
    def setup_book_display(self):
        # Titre du livre
        title_label = ctk.CTkLabel(
            self, 
            text=f"📖 {self.book.title}", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(anchor="w", pady=(10, 2), padx=15)
        
        # Date de publication
        date_label = ctk.CTkLabel(
            self, 
            text=f"📅 Date: {self.book.date}"
        )
        date_label.pack(anchor="w", pady=2, padx=15)
        
        # Prix
        price_label = ctk.CTkLabel(
            self, 
            text=f"💰 Price: {self.book.price} €"
        )
        price_label.pack(anchor="w", pady=2, padx=15)
        
        # collection
        collection_name = self.book.collection.name if self.book.collection else "No collection"
        collection_label = ctk.CTkLabel(
            self, 
            text=f"📦 Collection: {collection_name}"
        )
        collection_label.pack(anchor="w", pady=2, padx=15)
        
        # author_names = self.book_service.get_author_names_by_isbn(self.book.isbn)
        # author_text = ", ".join(author_names) if author_names else "Aucun auteur"
        # author_label = ctk.CTkLabel(
        #     self,
        #     text=f"✍️ Authors: {author_text}"
        # )
        # author_label.pack(anchor="w", pady=2, padx=15)
        
        # editor
        editor_names = ", ".join(editor.name for editor in self.book.editors)
        editor_label = ctk.CTkLabel(
            self, 
            text=f"🏢 editors: {editor_names}"
        )
        editor_label.pack(anchor="w", pady=2, padx=15)
        
        # # theme
        # theme_label = ctk.CTkLabel(
        #     self, 
        #     text=f"🏷️ theme: {self.book.theme}"
        # )
        # theme_label.pack(anchor="w", pady=2, padx=15)
        
        # Frame pour les boutons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", pady=10, padx=15)
        
        # Bouton supprimer
        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Supprimer",
            fg_color="red",
            hover_color="#cc0000",
            width=100,
            command=self.confirm_delete
        )
        delete_btn.pack(side="right", padx=(5, 0))
        
        # Bouton modifier
        if self.edit_callback:
            edit_btn = ctk.CTkButton(
                button_frame,
                text="✏️ Modifier",
                width=100,
                command=lambda: self.edit_callback(self.book)
            )
            edit_btn.pack(side="right", padx=(0, 5))
    
    def confirm_delete(self):
        """Confirmation avant suppression"""
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Confirmer la suppression")
        confirm_window.geometry("300x150")
        confirm_window.resizable(False, False)
        confirm_window.grab_set()  # Modal
        
        # Centrer la fenêtre
        confirm_window.transient(self.winfo_toplevel())
        
        # Message
        message = ctk.CTkLabel(
            confirm_window,
            text=f"Êtes-vous sûr de vouloir supprimer\n'{self.book.title}' ?",
            wraplength=250
        )
        message.pack(pady=20)
        
        # Boutons
        button_frame = ctk.CTkFrame(confirm_window, fg_color="transparent")
        button_frame.pack(pady=10)
        
        yes_btn = ctk.CTkButton(
            button_frame,
            text="Oui",
            fg_color="red",
            hover_color="#cc0000",
            command=lambda: [
                self.delete_callback(self.book),
                confirm_window.destroy()
            ]
        )
        yes_btn.pack(side="left", padx=10)
        
        no_btn = ctk.CTkButton(
            button_frame,
            text="Non",
            command=confirm_window.destroy
        )
        no_btn.pack(side="right", padx=10)

class BookPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.book_service = BookService()
        self.books = []
        self.filtered_books = []
        
        self.setup_ui()
        self.load_books()
        
    def setup_ui(self):
        # Configuration de la grille principale
        self.grid_rowconfigure(2, weight=1)  # La zone de liste s'étend
        self.grid_columnconfigure(0, weight=1)
        
        # === ZONE DE RECHERCHE ===
        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        search_frame.grid_columnconfigure(0, weight=1)
        search_frame.grid_columnconfigure(1, weight=0) 
        
        # Champ de recherche
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Rechercher par titre...",
            height=35
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        add_btn = ctk.CTkButton(
            search_frame,
            text="➕ ADD",
            command=self.add_book,
            height=35
        )
        add_btn.grid(row=0, column=3, padx=(5, 10), pady=10)
        
        # # === ZONE D'AJOUT ===
        # add_frame = ctk.CTkFrame(self)
        # add_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        # add_frame.grid_columnconfigure(0, weight=2)
        # add_frame.grid_columnconfigure(1, weight=1)
        # add_frame.grid_columnconfigure(2, weight=1)
        
        # # Champs d'ajout
        # self.title_entry = ctk.CTkEntry(add_frame, placeholder_text="Titre du livre")
        # self.title_entry.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=10)
        
        # self.date_entry = ctk.CTkEntry(add_frame, placeholder_text="Date (YYYY-MM-DD)")
        # self.date_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=10)
        
        # self.price_entry = ctk.CTkEntry(add_frame, placeholder_text="Price (€)")
        # self.price_entry.grid(row=0, column=2, sticky="ew", padx=5, pady=10)
        
        # # Bouton d'ajout
        # add_btn = ctk.CTkButton(
        #     add_frame,
        #     text="➕ Ajouter",
        #     command=self.add_book,
        #     height=35
        # )
        # add_btn.grid(row=0, column=3, padx=(5, 10), pady=10)
        
        # === ZONE DE LISTE SCROLLABLE ===
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600)
        self.scroll_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        # === ZONE D'INFORMATIONS ===
        info_frame = ctk.CTkFrame(self)
        info_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        self.info_label = ctk.CTkLabel(info_frame, text="", font=ctk.CTkFont(size=12))
        self.info_label.pack(pady=5)
    
    def load_books(self):
        """Charge tous les livres"""
        try:
            self.books = self.book_service.get_all()
            self.filtered_books = self.books.copy()
            self.display_books()
            self.update_info()
        except Exception as e:
            self.show_error(f"Erreur lors du chargement : {str(e)}")
    
    def display_books(self):
        """Affiche les livres dans la zone scrollable"""
        # Nettoyer les widgets existants
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        if not self.filtered_books:
            no_books_label = ctk.CTkLabel(
                self.scroll_frame,
                text="📚 Aucun livre trouvé",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            no_books_label.pack(pady=50)
            return
        
        # Afficher chaque livre
        for book in self.filtered_books:
            book_frame = BookFrame(
                self.scroll_frame,
                book,
                delete_callback=self.delete_book,
                edit_callback=self.edit_book  # Vous pouvez ajouter une fonction d'édition
            )
            book_frame.pack(fill="x", padx=10, pady=5)
    
    def edit_book(self,book):
        BookEditPage(book=book, on_success=self.refresh)
    
    def add_book(self):
        """Ajoute un nouveau livre"""
        title = self.title_entry.get().strip()
        date = self.date_entry.get().strip()
        price_str = self.price_entry.get().strip()
        
        # Validation
        if not title:
            self.show_error("Le titre est obligatoire")
            return
        
        if not date:
            self.show_error("La date est obligatoire")
            return
        
        try:
            price = float(price_str) if price_str else 0.0
        except ValueError:
            self.show_error("Le prix doit être un nombre valide")
            return
        
        try:
            # Créer un objet livre (ajustez selon votre modèle)
            # Supposons que BookService.create() accepte ces paramètres
            new_book = self.book_service.create(title=title, date=date, price=price)
            
            # Vider les champs
            self.title_entry.delete(0, 'end')
            self.date_entry.delete(0, 'end')
            self.price_entry.delete(0, 'end')
            
            # Recharger la liste
            self.load_books()
            self.show_success("Book successfully added !")
            
        except Exception as e:
            self.show_error(f"Error : {str(e)}")
    
    def delete_book(self, book):
        """Supprime un livre"""
        try:
            self.book_service.delete(book.id)  # Ajustez selon votre modèle
            self.load_books()
            self.show_success("Book successfully deleted !")
        except Exception as e:
            self.show_error(f"Error : {str(e)}")
    
    def on_search(self, event=None):
        """Filtre les livres selon la recherche"""
        query = self.search_entry.get().lower().strip()
        
        if not query:
            self.filtered_books = self.books.copy()
        else:
            self.filtered_books = [
                book for book in self.books
                if query in book.title.lower()
            ]
        
        self.display_books()
        self.update_info()
    
    def update_info(self):
        """Met à jour les informations affichées"""
        total = len(self.books)
        displayed = len(self.filtered_books)
        
        if total == displayed:
            info_text = f"📊 {total} book(s) total"
        else:
            info_text = f"📊 {displayed} book(s) displayed. {total} total"
        
        self.info_label.configure(text=info_text)
    
    def show_error(self, message):
        """Affiche un message d'erreur"""
        self.info_label.configure(text=f"❌ {message}", text_color="red")
        # Revenir à l'état normal après 3 secondes
        #self.after(3000, lambda: self.update_info())
    
    def show_success(self, message):
        """Affiche un message de succès"""
        self.info_label.configure(text=f"✅ {message}", text_color="green")
        # Revenir à l'état normal après 3 secondes
        self.after(3000, lambda: self.update_info())
    
    def refresh(self):
        """Méthode publique pour rafraîchir la page"""
        self.load_books()

