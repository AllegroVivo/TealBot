from __future__ import annotations

from datetime import datetime
from discord import Embed, EmbedField, User, Interaction
from typing import TYPE_CHECKING, Any, List, Optional, Tuple, Type, TypeVar

from .commission import TCommission
from ui import *
from utilities import *

if TYPE_CHECKING:
    pass
################################################################################

__all__ = (
    "TClient",
)

TC = TypeVar("TC", bound="TClient")

################################################################################
class TClient:

    __slots__ = (
        "_user",
        "_name",
        "_communication_method",
        "_commissions",
        "_tags",
        "_notes",
        "_update_date",
        "_email",
        "_paypal",
    )

################################################################################
    def __init__(
        self,
        user: User,
        name: Optional[str],
        communication_method: Optional[CommunicationMethod],
        tags: List[ClientTag],
        notes: Optional[str],
        update_date: datetime,
        email: Optional[str],
        paypal: Optional[str]
    ):

        self._user: User = user
        self._commissions: List[TCommission] = []

        self._name: str = name
        self._notes: Optional[str] = notes
        self._tags: List[ClientTag] = tags

        self._update_date: datetime = update_date
        self._communication_method: Optional[CommunicationMethod] = communication_method
        self._email: Optional[str] = email
        self._paypal: Optional[str] = paypal

################################################################################
    @classmethod
    def new(cls: Type[TC], user: User) -> TC:

        # Add to the database first.
        new_client_entry(user)

        return cls(
            user,
            None,
            None,
            [],
            None,
            datetime.now(),
            None,
            None
        )

################################################################################
    @classmethod
    def load(cls: Type[TC], user: User, data: Tuple[Any, ...]) -> TC:

        return cls(
            user,
            data[0],
            CommunicationMethod(data[4]) if data[4] else None,
            [],  # [ClientTag(tag) for tag in data[2].split(",")] if data[2] else [],
            data[1],
            data[3],
            data[5],
            data[6]
        )

################################################################################
    @property
    def mention(self) -> str:

        return self._user.mention

################################################################################
    @property
    def name(self) -> str:

        return self._name or self._user.display_name

################################################################################
    @name.setter
    def name(self, value: str) -> None:

        self._name = value
        self.update()

################################################################################
    @property
    def notes(self) -> Optional[str]:

        return self._notes

################################################################################
    @notes.setter
    def notes(self, value: Optional[str]) -> None:

        self._notes = value
        self.update()

################################################################################
    @property
    def tags(self) -> List[ClientTag]:

        return self._tags

################################################################################
    @tags.setter
    def tags(self, value: List[ClientTag]) -> None:

        self._tags = value
        self.update()

################################################################################
    @property
    def communication_method(self) -> Optional[CommunicationMethod]:

        return self._communication_method

################################################################################
    @communication_method.setter
    def communication_method(self, value: Optional[CommunicationMethod]) -> None:

        self._communication_method = value
        self.update()

################################################################################
    @property
    def email(self) -> Optional[str]:

        return self._email

################################################################################
    @email.setter
    def email(self, value: Optional[str]) -> None:

        self._email = value
        self.update()

################################################################################
    @property
    def paypal(self) -> Optional[str]:

        return self._paypal

################################################################################
    @paypal.setter
    def paypal(self, value: Optional[str]) -> None:

        self._paypal = value
        self.update()

################################################################################
    def status(self) -> Embed:

        comm_pref = self.communication_method.proper_name if self.communication_method else str(NS)
        tags_val = "- " + "\n- ".join([tag.proper_name for tag in self.tags])
        email_val = self._email if self._email else str(NS)
        paypal_val = self._paypal if self._paypal else str(NS)
        notes_val = self._notes if self._notes else str(NS)

        fields = [
            EmbedField("__Discord User__", self.mention, True),
            EmbedField("__Communication Pref.__", comm_pref, True),
            EmbedField("** **", "** **", False),
            EmbedField("__Email__", email_val, True),
            EmbedField("__PayPal__", paypal_val, True),
            EmbedField("** **", "** **", False),
            EmbedField("__Tags__", tags_val, True),
            EmbedField("__Notes__", notes_val, True)
        ]

        return make_embed(
            title=f"Client Overview: {self.name}",
            description=(
                f"{draw_separator(extra=30)}\n"
                "Commission Information Goes Here Eventually\n"
                f"{draw_separator(extra=30)}"
            ),
            footer_text=f"Client Last Updated: {self._update_date.strftime('%m/%d/%Y')}",
            fields=fields
        )

################################################################################
    async def main_menu(self, interaction: Interaction) -> None:

        status = self.status()
        view = ClientStatusView(interaction.user, self)

        await interaction.response.send_message(embed=status, view=view)
        await view.wait()

        return

################################################################################
    async def set_name(self, interaction: Interaction) -> None:

        modal = ClientNameModal(self._name)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.name = modal.value

        return

################################################################################
    async def set_email(self, interaction: Interaction) -> None:

        modal = ClientEmailModal(self._email)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.email = modal.value

        return

################################################################################
    async def set_paypal(self, interaction: Interaction) -> None:

        modal = ClientPaypalModal(self._paypal)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.paypal = modal.value

        return

################################################################################
    async def set_notes(self, interaction: Interaction) -> None:

        modal = ClientNotesModal(self._notes)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.notes = modal.value

        return

################################################################################
    async def set_communication_method(self, interaction: Interaction) -> None:

        embed = make_embed(
            title="Set Communication Method",
            description=(
                "Please select the preferred communication method for this client."
            )
        )
        view = CommunicationMethodView(interaction.user)

        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()

        if not view.complete:
            return

        self.communication_method = CommunicationMethod(view.value)

        return

################################################################################
    async def set_tags(self, interaction: Interaction) -> None:

        embed = make_embed(
            title="Set Client Tags",
            description=(
                "Please select the tags that apply to this client."
            )
        )
        view = ClientTagSelectView(interaction.user)

        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()

        if not view.complete:
            return

        self.tags = [ClientTag(tag) for tag in view.value]

        return

################################################################################
    def update(self) -> None:

        self._update_date = datetime.now()

        c = db_connection.cursor()
        c.execute(
            "UPDATE clients SET name = %s, communication_method = %s, "
            "notes = %s, tags = %s, update_date = %s, email = %s, paypal = %s "
            "WHERE user_id = %s",
            (
                self._name, self._communication_method.value, self._notes,
                self._tags,
                self._update_date, self._email, self._paypal, self._user.id
            )
        )

        db_connection.commit()
        c.close()

        return

################################################################################
