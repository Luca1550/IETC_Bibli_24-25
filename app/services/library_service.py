import re
from repositories.models import Library
from repositories import LibraryRepo

class LibraryService:
    """
    Service for managing libraries.
    Provides methods to retrieve library parameters.
    Uses LibraryRepo for data access.
    """

    def __init__(self):
        """
        Initializes the LibraryService instance.
        """
        self._library_repo : LibraryRepo = LibraryRepo()

    def get_library_parameters(self):
        """
        Retrieves the parameters of the library.
        Returns:
            list[Library]: A list of library objects.
        """
        return self._library_repo.get_library_parameters()
    
    def add_library(self,name: str, fine_per_day: float, subscribe_amout: float, limit_borrow: int, borrow_price_with_sub: float, borrow_price_without_sub: float, borrow_delay: int, url_logo: str, id: int | None = None) -> Library:
        """
        Adds a new library to the repository.
        Args:
            name (str): Name of the library.
            fine_per_day (float): Fine charged per day for overdue items.
            subscribe_amout (float): Subscription amount for the library.
            limit_borrow (int): Maximum number of items that can be borrowed at once.
            borrow_price_with_sub (float): Borrowing price for subscribers.
            borrow_price_without_sub (float): Borrowing price for non-subscribers.
            borrow_delay (int): Allowed borrowing delay in days.
            url_logo (str): URL to the library's logo image.
        Returns:        
            Library: The added library object.
        """    
        try:
            if not fine_per_day >= 0 or  not isinstance(fine_per_day, (int, float)):
                raise Exception("Invalid fine per day: it must be a non-negative numeric value.")
            if not subscribe_amout >= 0 or not isinstance(subscribe_amout, (int, float)):
                raise Exception("Invalid subscription amount: it must be a non-negative numeric value.")
            if not limit_borrow >= 0 or not isinstance(limit_borrow, (int)):
                raise Exception("Invalid limit borrow: it must be a non-negative numeric value.")
            if not borrow_price_with_sub >= 0 or not borrow_price_with_sub(fine_per_day, (int, float)):
                raise Exception("Invalid borrow price with subscription: it must be a non-negative numeric value.")
            if not borrow_price_without_sub >= 0 or not isinstance(borrow_price_without_sub, (int, float)):
                raise Exception("Invalid borrow price without subscription: it must be a non-negative numeric value.")
            if not borrow_delay >= 0 or not isinstance(borrow_delay, (int)):
                raise Exception("Invalid borrow delay: it must be a non-negative numeric value.")
            
            url_pattern = re.compile(r'^https?://[\w\-\.]+\.\w{2,}(?:/[\w\-/\.\?\=\&]*)?$')
            if not isinstance(url_logo, str) or not url_pattern.match(url_logo):
                raise ValueError("Invalid URL for logo: it must be a valid URL.")
            
            new_library = Library(
                id=None,  
                name=name,
                fine_per_day=fine_per_day,
                subscribe_amout=subscribe_amout,
                limit_borrow=limit_borrow,
                borrow_price_with_sub=borrow_price_with_sub,
                borrow_price_without_sub=borrow_price_without_sub,
                borrow_delay=borrow_delay,
                url_logo=url_logo
            )
            return self._library_repo.add_library(new_library)
        except Exception as e:
            return f"🛑 Error [{e}]"