from __future__ import annotations

from discord import ButtonStyle, Embed, Interaction, Member, NotFound, User
from discord.ext.pages import Page, Paginator
from discord.ui import Button, button, Modal
from typing import TYPE_CHECKING, Any, List, Optional, Union

from .view import TealView

if TYPE_CHECKING:
    from classes.commissions import TClientManager, TCommissionManager, TCommissionTypeManager
################################################################################

__all__ = (
    "ConfirmCancelView",
    "CloseMessageButton",
    "CloseMessageView",
    "TSectionButton",
    "TealModal",
    "Frogginator"
)

################################################################################
class ConfirmCancelView(TealView):

    def __init__(self, owner: Union[Member, User], *args, **kwargs):

        super().__init__(owner, *args, close_on_complete=True, **kwargs)

    @button(
        style=ButtonStyle.success,
        label="Confirm",
        disabled=False,
        row=0
    )
    async def confirm(self, btn: Button, interaction: Interaction):
        self.value = True
        self.complete = True

        await interaction.response.edit_message()
        await self.stop()  # type: ignore

    @button(
        style=ButtonStyle.danger,
        label="Cancel",
        disabled=False,
        row=0
    )
    async def cancel(self, btn: Button, interaction: Interaction):
        self.value = False
        self.complete = True

        await interaction.response.edit_message()
        await self.stop()  # type: ignore

################################################################################
class CloseMessageButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.success,
            label="Close Message",
            disabled=False,
            row=4
        )

    async def callback(self, interaction: Interaction):
        self.view.value = True
        self.view.complete = True
        self.view._close_on_complete = True

        await interaction.response.edit_message()

        if isinstance(self.view, Paginator):
            await self.view.cancel()
        else:
            await self.view.stop()  # type: ignore

################################################################################
class CloseMessageView(TealView):

    def __init__(self, owner: Union[Member, User]):
        super().__init__(owner, close_on_complete=True)

        self.add_item(CloseMessageButton())

################################################################################
class TSectionButton(Button):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

################################################################################
    def set_style(self, attribute: Optional[Any]) -> None:

        if attribute:
            self.style = ButtonStyle.primary
        else:
            self.style = ButtonStyle.secondary

################################################################################
class TealModal(Modal):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.complete: bool = False
        self.value: Optional[Any] = None

################################################################################
class Frogginator(Paginator):

    def __init__(
        self,
        pages: List[Page],
        obj_ref: Union[TClientManager, TCommissionManager, TCommissionTypeManager],
        close_on_complete: bool = False,
        **kwargs
    ):

        super().__init__(pages=pages, author_check=True, **kwargs)

        self.obj_ref: Union[TClientManager, TCommissionManager, TCommissionTypeManager] = obj_ref
        self._interaction: Optional[Interaction] = None
        self._close_on_complete: bool = close_on_complete

################################################################################
    async def interaction_check(self, interaction: Interaction) -> bool:

        self._interaction = interaction
        return await super().interaction_check(interaction)

################################################################################
    async def on_timeout(self) -> None:

        try:
            await super().on_timeout()
        except NotFound:
            pass
        except:
            raise

################################################################################
    async def cancel(
        self,
        include_custom: bool = False,
        page: Optional[str, Page, List[Embed], Embed] = None,
    ) -> None:

        if self._close_on_complete:
            if self._interaction is not None:
                try:
                    await self.message.delete()
                except:
                    print("Error in Frogginator Cancel")
        else:
            await super().cancel(include_custom, page)

################################################################################
