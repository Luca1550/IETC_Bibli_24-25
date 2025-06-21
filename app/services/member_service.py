import re
from repositories.models import Member, Person
from repositories import MemberRepo, PersonRepo
from services import PersonService
from services.models import MemberDTO
from datetime import date
from typing import Optional

class MemberService:
    """
    Service for managing Member objects.
    """

    def __init__(self):
        self._member_repo = MemberRepo()
        self._person_repo = PersonRepo()
        self._person_service = PersonService()


    def add_member(self, id : int, first_name : str, last_name : str, national_number: str, email : str, street : str, cp : str, city : str, membership_entrydate : date, subscribed : bool, archived : bool) -> MemberDTO:
        """
        Adds a Member object to the repository.
        :param member: Member object to be added.
        :return: True if the member was added successfully, False otherwise.
        """
        person = self._person_service.add_person(
            first_name,
            last_name,
            national_number,
            email,
            street,
            cp,
            city
        )
        if isinstance(person, Person):
            member = Member(
                id=id,
                id_person=person.id,
                membership_entrydate=membership_entrydate,
                subscribed=subscribed,
                archived=archived
            )
            self._member_repo.add_member(member)
            return MemberDTO(
                id_member=member.id,
                person=person,
                membership_entrydate=member.membership_entrydate,
                subscribed=member.subscribed,
                archived=member.archived
            )
        else:
            raise Exception("Failed to add person.")

    def update_member(self, id: int, first_name: str, last_name: str, national_number: str, email: str, street: str, cp: str, city: str, membership_entrydate: date, subscribed: bool, archived: bool) -> bool:
        success = self._person_service.update_person(
            id,
            first_name,
            last_name,
            national_number,
            email,
            street,
            cp,
            city
        )
        if success:
            # Récupérer le membre existant, pas créer un nouveau
            member = self._member_repo.get_member_by_id(id)
            if not member:
                raise Exception("Member not found for update.")
            
            # Mettre à jour les champs du membre existant
            member.membership_entrydate = membership_entrydate
            member.subscribed = subscribed
            member.archived = archived
            
            # Sauvegarder le membre mis à jour dans le repo
            self._member_repo.update_member(member)
            return True

        raise Exception("Person update failed.")

    def get_member_by_id(self, id: int) -> MemberDTO | None:
        """
        Retrieves a Member object by its ID.
        :param id: ID of the Member to retrieve.
        :return: Member object if found, None otherwise.
        """
        member = self._member_repo.get_member_by_id(id)
        if member:
            person = self._person_repo.get_by_id(member.id_person)
            if person:
                return MemberDTO(
                    id_member=member.id,
                    person=person,
                    membership_entrydate=member.membership_entrydate,
                    subscribed=member.subscribed,
                    archived=member.archived
                )
        return None

    def delete_member(self, id: int) -> bool:
        """
        Deletes a Member object from the repository.
        :param member: Member object to be deleted.
        :return: True if the member was deleted successfully, False otherwise.
        """
        try:
            member = self._member_repo.get_member_by_id(id)
            if member:
                self._member_repo.delete_member(member)
                self._person_service.delete_person(member.id_person)
                return True
            else:
                raise Exception(f"Member with the given ID : {id} was not found.")
        except Exception as e:
            raise(f"🛑 Error [{e}]")
            return False
        
    def get_all_members(self) -> list[MemberDTO]:
        """
        Retrieves all Member objects from the repository.
        :return: A list of all Member objects.
        """
        members = self._member_repo.get_all_members()
        member_dtos = []
        for member in members:
            person = self._person_repo.get_by_id(member.id_person)
            if person:
                member_dtos.append(MemberDTO(
                    id_member=member.id,
                    person=person,
                    membership_entrydate=member.membership_entrydate,
                    subscribed=member.subscribed,
                    archived=member.archived
                ))
        return member_dtos