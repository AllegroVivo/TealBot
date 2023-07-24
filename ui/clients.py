from __future__ import annotations

from discord import ButtonStyle, InputTextStyle, Interaction, Member, SelectOption, User
from discord.ext.pages import Paginator
from discord.ui import Button, button, InputText, Select
from typing import TYPE_CHECKING, List, Optional

from .common import *
from utilities import *
from .view import TealView

if TYPE_CHECKING:
    from classes.commissions import TClient
################################################################################

__all__ = (
    "ClientStatusView",
    "ClientNameModal",
    "ClientEmailModal",
    "ClientPaypalModal",
    "ClientNotesModal",
    "CommunicationMethodView",
    "ClientTagSelectView",
)

################################################################################
class ClientNameModal(TealModal):

    def __init__(self, cur_val: Optional[str] = None):
        super().__init__(title="Edit Client Name")

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Client Name",
                placeholder="Allegro Vivo, Frog Mistress!",
                required=True,
                max_length=50,
                value=cur_val
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[0].value
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
class ClientEmailModal(TealModal):

    def __init__(self, cur_val: Optional[str] = None):
        super().__init__(title="Edit Client Email")

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Client Email",
                placeholder="eg. 'allegro@discordqueen.com'",
                required=False,
                value=cur_val
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[0].value if self.children[0].value else None
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
class ClientPaypalModal(TealModal):

    def __init__(self, cur_val: Optional[str] = None):
        super().__init__(title="Edit Client Paypal")

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Client Paypal",
                placeholder="eg. 'paypalemail@gmail.com'",
                required=False,
                value=cur_val
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[0].value if self.children[0].value else None
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
class ClientNotesModal(TealModal):

    def __init__(self, cur_val: Optional[str] = None):
        super().__init__(title="Edit Client Notes")

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Client Notes",
                placeholder="eg. 'Likes frogs, hates cats'",
                required=False,
                value=cur_val
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[0].value if self.children[0].value else None
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################
class ClientNameButton(TSectionButton):

    def __init__(self, cur_val: Optional[str] = None):

        super().__init__(
            label="Name",
            disabled=False,
            row=0
        )

        self.set_style(cur_val)

    async def callback(self, interaction: Interaction):

        client: TClient = self.view.client
        await client.set_name(interaction)

        self.set_style(client._name)

        await edit_message_helper(
            interaction,
            embed=client.status(),
            view=self.view
        )

################################################################################
class ClientEmailButton(TSectionButton):

    def __init__(self, cur_val: Optional[str] = None):
        super().__init__(
            label="Email",
            disabled=False,
            row=1
        )

        self.set_style(cur_val)

    async def callback(self, interaction: Interaction):

        client: TClient = self.view.client
        await client.set_email(interaction)

        self.set_style(client._email)

        await edit_message_helper(
            interaction,
            embed=client.status(),
            view=self.view
        )

################################################################################
class ClientPaypalButton(TSectionButton):

    def __init__(self, cur_val:Optional[str] = None):
        super().__init__(
            label="Paypal",
            disabled=False,
            row=1
        )

        self.set_style(cur_val)

    async def callback(self, interaction: Interaction):

        client: TClient = self.view.client
        await client.set_paypal(interaction)

        self.set_style(client._paypal)

        await edit_message_helper(
            interaction,
            embed=client.status(),
            view=self.view
        )

################################################################################
class ClientNotesButton(TSectionButton):

    def __init__(self, cur_val:Optional[str] = None):
        super().__init__(
            label="Notes",
            disabled=False,
            row=1
        )

        self.set_style(cur_val)

    async def callback(self, interaction: Interaction):

        client: TClient = self.view.client
        await client.set_notes(interaction)

        self.set_style(client._notes)

        await edit_message_helper(
            interaction,
            embed=client.status(),
            view=self.view
        )

################################################################################
class ClientCommunicationButton(TSectionButton):

    def __init__(self, cur_val: Optional[CommunicationMethod] = None):
        super().__init__(
            label="Communication Method",
            disabled=False,
            row=0
        )

        self.set_style(cur_val)

    async def callback(self, interaction: Interaction):

        client: TClient = self.view.client
        await client.set_communication_method(interaction)

        self.set_style(client._notes)

        await edit_message_helper(
            interaction,
            embed=client.status(),
            view=self.view
        )

################################################################################
class ClientTagsButton(TSectionButton):

    def __init__(self, cur_val: Optional[List[ClientTag]] = None):
        super().__init__(
            label="Tags",
            disabled=False,
            row=1
        )

        self.set_style(cur_val)

    async def callback(self, interaction: Interaction):

        client: TClient = self.view.client
        await client.set_tags(interaction)

        self.set_style(client._tags)

        await edit_message_helper(
            interaction,
            embed=client.status(),
            view=self.view
        )

################################################################################
class ClientStatusView(TealView):

    def __init__(self, owner: User, client: TClient):
        super().__init__(owner)

        self.client: TClient = client

        buttons = [
            ClientNameButton(self.client._name),
            ClientCommunicationButton(self.client._communication_method),
            ClientEmailButton(self.client._email),
            ClientPaypalButton(self.client._paypal),
            ClientTagsButton(self.client._tags),
            ClientNotesButton(self.client._notes),
            CloseMessageButton()
        ]

        for btn in buttons:
            self.add_item(btn)

################################################################################
class CommunicationMethodSelect(Select):

    def __init__(self):
        super().__init__(
            placeholder="Select a communication method",
            options=CommunicationMethod.select_options()
        )

    async def callback(self, interaction: Interaction):
        self.view.value = int(self.values[0])
        self.view.complete = True

        await interaction.response.edit_message()
        await self.view.stop()  # type: ignore

################################################################################
class CommunicationMethodView(TealView):

    def __init__(self, owner: User):
        super().__init__(owner, close_on_complete=True)

        self.add_item(CommunicationMethodSelect())

################################################################################
class ClientTagSelect(Select):

    def __init__(self):
        super().__init__(
            placeholder="Select a tag",
            options=ClientTag.select_options(),
            max_values=len(ClientTag.select_options())
        )

    async def callback(self, interaction: Interaction):
        self.view.value = [int(v) for v in self.values]
        self.view.complete = True

        await interaction.response.edit_message()
        await self.view.stop()  # type: ignore

################################################################################
class ClientTagSelectView(TealView):

    def __init__(self, owner: User):
        super().__init__(owner, close_on_complete=True)

        self.add_item(ClientTagSelect())

################################################################################
