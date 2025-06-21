from repositories.models import Person

class MemberDTO:
    """
    Data Transfer Object for Member.
    This class is used to transfer member data between different layers of the application.
    """
    def __init__(self, id_member: int, person: Person, membership_entrydate: str, subscribed : bool , archived: bool):
        """
        Initializes a MemberDTO instance with the provided parameters.
        :param id_member: Unique identifier for the member.
        :param person: Person object containing personal details of the member.
        """
        self.id_member = id_member
        self.person = person
        self.membership_entrydate = membership_entrydate
        self.subscribed = subscribed
        self.archived = archived

    def __eq__(self, other):
        """
        Compares two MemberDTO objects for equality based on their ID.
        arguments:
            other (MemberDTO): The other MemberDTO object to compare with.
        """
        if isinstance(other, MemberDTO):
            return self.id_member == other.id_member

    def __hash__(self):
        """
        Returns a hash value for the MemberDTO object based on its ID."""
        
        return hash(self.id_member)