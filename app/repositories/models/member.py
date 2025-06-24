from repositories.models import Base

class Member(Base):
    """
    Represents a member in the system.
    """
    def __init__(self, id: int | None, id_person: int, membership_entrydate: str, subscribed : bool = False, archived: bool = False):
        """
        Member model representing a member in the system.
        :param id: Unique identifier for the member, can be None if not yet created.
        :param id_person: Unique identifier for the associated person.
        :param membership_entrydate: Entry date of the membership.
        :param subscribed: Indicates if the member is subscribed.
        :param archived: Indicates if the member is archived.
        """
        super().__init__(id)
        self.id_person = id_person
        self.membership_entrydate = membership_entrydate
        self.subscribed = subscribed
        self.archived = archived
