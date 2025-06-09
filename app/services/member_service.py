import re
from repositories.models import Member
from repositories.models import Person
from repositories import MemberRepo
from repositories import PersonRepo

class MemberService:
    """
    Service for managing Member objects.
    """

    def __init__(self):
        self._member_repo = MemberRepo()
        self._person_repo = PersonRepo()

    def add_member(self, member: Member) -> bool:
        """
        Adds a Member object to the repository.
        :param member: Member object to be added.
        :return: True if the member was added successfully, False otherwise.
        """
        return self._member_repo.add_member(member)

    def update_member(self, member: Member) -> bool:
        """
        Updates an existing Member object in the repository.
        :param member: Member object to be updated.
        :return: True if the member was updated successfully, False otherwise.
        """
        return self._member_repo.update_member(member)

    def get_member_by_id(self, id: int) -> Member | None:
        """
        Retrieves a Member object by its ID.
        :param id: ID of the Member to retrieve.
        :return: Member object if found, None otherwise.
        """
        return self._member_repo.get_member_by_id(id)

    def delete_member(self, member: Member) -> bool:
        """
        Deletes a Member object from the repository.
        :param member: Member object to be deleted.
        :return: True if the member was deleted successfully, False otherwise.
        """
        return self._member_repo.delete_member(member)

    def get_all_members(self) -> list[Member]:
        """
        Retrieves all Member objects from the repository.
        :return: A list of all Member objects.
        """
        return self._member_repo.get_all_members()