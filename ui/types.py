from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from discord import ButtonStyle, Embed, InputTextStyle, Interaction, NotFound, User
from discord.ext.pages import Page, Paginator
from discord.ui import Button, InputText, View

from utilities import *
from .common import *
from .view import TealView

if TYPE_CHECKING:
    from classes.commissions import TCommissionType, TCommissionTypeManager
################################################################################

__all__ = (
    "CommissionTypeModal",
    "CommissionTypeStatusView",
)

################################################################################
class CommissionTypeModal(TealModal):

    def __init__(
        self,
        name: Optional[str] = None,
        price: Optional[int] = None,
        description: Optional[str] = None
    ):
        super().__init__(title="Edit Commission Type")

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Item Name",
                placeholder="eg. 'Chibify'",
                required=True,
                value=name
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Price",
                placeholder="eg. '50'",
                required=True,
                value=str(price) if price else None
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Description",
                placeholder="eg. 'Turns you into a chibi.' (This is optional~)",
                required=False,
                value=description
            )
        )

    async def callback(self, interaction: Interaction):
        name = self.children[0].value
        description = self.children[2].value if self.children[2].value else None

        try:
            price = int(self.children[1].value)
        except ValueError:
            error = InvalidNumberError(self.children[1].value)
            await interaction.response.send_message(embed=error, ephemeral=True)
            return

        await interaction.response.send_message("** **", delete_after=0.1)

        self.value = (name, price, description)
        self.complete = True

################################################################################
class EditCommTypeButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.primary,
            label="Edit",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        await self.view.comm_type.set_values(interaction)

        await edit_message_helper(
            interaction=interaction,
            embed=self.view.comm_type.status(),
            view=self.view
        )

################################################################################
class RemoveCommTypeButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.danger,
            label="Remove",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        await self.view.comm_type.remove(interaction)

        self.view._close_on_complete = True
        self.view.complete = True

        await self.view.stop()  # type: ignore

################################################################################
class AddCommTypeImageButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.primary,
            label="Add Image",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        await self.view.comm_type.set_image(interaction)

        await edit_message_helper(
            interaction=interaction,
            embed=self.view.comm_type.status(),
            view=self.view
        )

################################################################################
class CommissionTypeStatusView(TealView):

    def __init__(self, owner: User, comm_type: TCommissionType):
        super().__init__(owner)

        self.comm_type = comm_type

        button_list = [
            EditCommTypeButton(),
            AddCommTypeImageButton(),
            RemoveCommTypeButton(),
            CloseMessageButton()
        ]

        for btn in button_list:
            self.add_item(btn)

################################################################################
