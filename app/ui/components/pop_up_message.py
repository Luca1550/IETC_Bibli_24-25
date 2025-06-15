import customtkinter

class PopUpMessage(customtkinter.CTkToplevel):
    """
    A pop-up message window that displays a message to the user.
    """
    def __init__(self, parent, message: str):
        """
        Initializes a pop-up message window with a given message.
        If the message contains "error", it will be displayed in red; otherwise, it will be in blue.
        arguments:
        - parent: The parent window for the pop-up.
        - message: The message to be displayed in the pop-up.
        This pop-up will always be on top of the parent window and will require user interaction to close.
        """
        super().__init__(parent)
        self.geometry("600x200")
        self.title("Notification")
        self.focus_set()
        self.grab_set()
        self.lift()
        self.attributes("-topmost", True) 

        if "error" in message.lower():
            self.label = customtkinter.CTkLabel(self, text=message, fg_color="red", text_color="white", corner_radius=10)
        else:
            self.label = customtkinter.CTkLabel(self, text=message, fg_color="#1f6aa5", text_color="white", corner_radius=10)
        self.label.pack(pady=20, padx=20, fill="both", expand=True)

        close_button = customtkinter.CTkButton(self, text="OK", command=self.destroy)
        close_button.pack(pady=10)

    @staticmethod
    def pop_up(parent, message: str):
        """
        Displays a pop-up message with the given message.
        If the message contains "error", it will be displayed in red; otherwise, it will be in blue.
        arguments:
        - parent: The parent window for the pop-up.
        - message: The message to be displayed in the pop-up.
        returns:
        - True if the message was displayed successfully, False otherwise.
        This method creates a new instance of PopUpMessage and waits for it to be closed.
        """
        popup = PopUpMessage(parent, message)
        popup.wait_window()
        return "error" not in message.lower()