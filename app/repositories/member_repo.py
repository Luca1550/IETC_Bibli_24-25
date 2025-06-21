import pathlib
from repositories.models import Member
from tools import JsonStorage

class MemberRepo:
    """
    Repository for managing Member objects.
    arguments:
    - PATH_MEMBER_JSON: Path to the JSON file where Member data is stored.
    """
    PATH_MEMBER_JSON = pathlib.Path(__file__).parent.parent.parent / "database" / "member.json"

    _member_json: list[Member] = JsonStorage.load_all(PATH_MEMBER_JSON)
    def __init__(self):
        """
        Initializes the MemberRepo instance and loads all Member data from the JSON file.
        If the JSON file does not exist, it initializes an empty list for Member data.
        """

    def _save_all(self):
        """
        Saves all Member data to the JSON file.
        """
        JsonStorage.save_all(self.PATH_MEMBER_JSON, self._member_json)

    def add_member(self, member: Member) -> bool:
        """
        Adds a Member object to the repository and saves it to the JSON file.
        arguments:
        - member: Member object to be added.
        returns:
        - True if the member was added successfully, False otherwise.
        """
        if isinstance(member, Member):
            self._member_json.append(member)
            self._save_all()
            return True
        return False
    
    def update_member(self, member: Member) -> bool:
        """
        Updates an existing Member object in the repository and saves the changes to the JSON file.
        arguments:
        - member: Member object to be updated.
        returns:
        - True if the member was updated successfully, otherwise returns False.
        """
        if isinstance(member, Member):
            index = next((i for i, m in enumerate(self._member_json) if m.id == member.id), None)
            if index is not None:
                self._member_json[index] = member
                self._save_all()
                return True
        return False
    
    def get_member_by_id(self, id: int) -> Member | None:
        """
        Retrieves a Member object by its ID.
        arguments:
        - id: ID of the Member to retrieve.
        returns:
        - Returns the Member object if found, otherwise returns None.
        """
        if id:
            return next((m for m in self._member_json if m.id == id), None)
        return None
    
    def delete_member(self, member: Member) -> bool:
        """
        Deletes a Member object from the repository and saves the changes to the JSON file.
        arguments:
        - member: Member object to be deleted.
        returns:
        - True if the member was deleted successfully, otherwise returns False.
        """
        if isinstance(member, Member):
            try:
                self._member_json.remove(member)
                self._save_all()
                return True
            except ValueError:
                return False
        return False

    def get_all_members(self) -> list[Member]:
        """
        Retrieves all Member objects from the repository.
        returns:
        - A list of all Member objects.
        """
        self._member_json = JsonStorage.load_all(self.PATH_MEMBER_JSON)
        return self._member_json