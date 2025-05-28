import customtkinter as ctk
import os
from services import PersonService
from ui.components import PopUpMessage

class PersonAddPage(ctk.CTkToplevel):
    """
    Page to add a new person.
    This page allows the user to input details for a new person and save them.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the PersonAddPage with a title, geometry, and various input fields.
        The page includes fields for first name, last name, national number, email, street, postal code, and city.
        It also includes a confirm button to save the new person and a cancel button to close the page.
        """
        super().__init__(*args, **kwargs)
        self.geometry("500x520")
        self.title("Add a new person")
        self._person_service : PersonService = PersonService()
        
        self.font=("Roboto" if os.name == "nt" else "SF Display", 20)

        label_title = ctk.CTkLabel(self, text="➕ Add a new person 👨", anchor="w", height=50, font=self.font)
        label_title.pack(fill="x", padx="15")  

        divider = ctk.CTkFrame(self, height=2, fg_color="gray")
        divider.pack(fill="x", padx="15", pady="15")

        label_first_name = ctk.CTkLabel(self, text="First name", anchor="w")
        label_first_name.pack(fill="x", padx="15")  
        self.input_fisrt_name = ctk.CTkEntry(self)
        self.input_fisrt_name.pack(fill="x", padx="15")
        
        label_last_name = ctk.CTkLabel(self, text="Last name", anchor="w")
        label_last_name.pack(fill="x", padx="15")  
        self.input_last_name = ctk.CTkEntry(self)
        self.input_last_name.pack(fill="x", padx="15")

        label_national_number = ctk.CTkLabel(self, text="National Number", anchor="w")
        label_national_number.pack(fill="x", padx="15")  
        self.input_national_number = ctk.CTkEntry(self)
        self.input_national_number.pack(fill="x", padx="15")

        label_email = ctk.CTkLabel(self, text="Email", anchor="w")
        label_email.pack(fill="x", padx="15")  
        self.input_email = ctk.CTkEntry(self)
        self.input_email.pack(fill="x", padx="15")

        label_street = ctk.CTkLabel(self, text="Street", anchor="w")
        label_street.pack(fill="x", padx="15")  
        self.input_street = ctk.CTkEntry(self)
        self.input_street.pack(fill="x", padx="15")

        container_frame = ctk.CTkFrame(self, fg_color="transparent")
        container_frame.pack(fill="x")

        left_frame_cp = ctk.CTkFrame(container_frame, fg_color="transparent")
        left_frame_cp.pack(side="left", fill="both")
        label_cp = ctk.CTkLabel(left_frame_cp, text="Postal code")
        label_cp.pack( padx="15", anchor="w") 
        self.input_cp = ctk.CTkEntry(left_frame_cp, width=100)
        self.input_cp.pack( padx="15", fill="x")

        right_frame_city = ctk.CTkFrame(container_frame, fg_color="transparent")
        right_frame_city.pack(side="right", fill="both", expand=True)
        label_city = ctk.CTkLabel(right_frame_city, text="City") 
        label_city.pack( padx="15", anchor="w") 
        self.input_city = ctk.CTkEntry(right_frame_city) 
        self.input_city.pack( padx="15", fill="x")

        divider_footer = ctk.CTkFrame(self, height=2, fg_color="gray")
        divider_footer.pack(fill="x", padx=15, pady=15)

        confirm_button = ctk.CTkButton(self, text="Confirm", command=self.confirm_action)
        confirm_button.pack(fill="x", padx=15)

        cancel_button = ctk.CTkButton(self, text="Cancel", fg_color="transparent", border_width=2, border_color="#1f6aa5")
        cancel_button.pack(fill="x", padx=15, pady=10)

    def confirm_action(self):
        """
        Validates the input fields and adds a new person using the PersonService.
        If the person is added successfully, the page is closed.
        If there is an error, a pop-up message is displayed with the error details.
        """
        new_person = self._person_service.add_person(
            first_name=self.input_fisrt_name.get(),
            last_name=self.input_last_name.get(),
            national_number=self.input_national_number.get(), 
            email=self.input_email.get(),
            street=self.input_street.get(),
            cp=self.input_cp.get(),
            city=self.input_city.get())
        if isinstance(new_person, str):
            PopUpMessage.pop_up(self, new_person)
        else:
            PopUpMessage.pop_up(self, f"Person {new_person.first_name} {new_person.last_name} added successfully. ✅")
            self.destroy()
        
