import pathlib
from repositories.models import Borrow
from tools import JsonStorage

class BorrowRepository:
    PATH_BORROW_JSON=pathlib.Path(__file__).parent.parent.parent / "database" / "borrow.json"

    def __init__(self):
        self.borrow_json : list[Borrow] = JsonStorage.load_all(self.PATH_BORROW_JSON)
        if self.borrow_json is None:
            self.borrow_json = []

    def add_borrow(self, borrow: Borrow):
        if borrow:
            self.borrow_json.append(borrow)
            self._save_all()
            return True
        return False 

    def get_borrows(self):
        return self.borrow_json

    def update_borrow(self, borrow: Borrow):
        if isinstance(borrow, Borrow):
            self.borrow_json[self.borrow_json.index(borrow)] = borrow
            self._save_all()
            return True
        return False

    def delete_borrow(self, borrow: Borrow):
        if isinstance (borrow, Borrow):
            self.book_json.remove(borrow)
            self._save_all()
            return True
        return False
    
    def check_limit_borrow(self):
        pass 
    def calculate_fine(self, borrow: Borrow):
        if borrow.return_date and borrow.borrow_date:
            days_overdue = (borrow.return_date - borrow.borrow_date).days
            if days_overdue > 0:
                #je dois remplacer le chiffre par le truc de library
                return days_overdue * 900000000