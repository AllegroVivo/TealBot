from __future__ import annotations

from discord import Embed, EmbedField, Interaction
from discord.ext.pages import Page
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Type, TypeVar

from .comm_type import TCommissionType
from ui.common import *
from ui.types import *
from utilities import *

if TYPE_CHECKING:
    from classes.bot import TealBot
################################################################################

__all__ = (
    "CommissionTypeManager"
)

################################################################################
class TCommissionTypeManager:

    __slots__ = (
        "_parent",
        "_types",
    )

################################################################################
    def __init__(self, parent: TealBot):

        self._parent: TealBot = parent
        self._types: Dict[int, TCommissionType] = {}  # Maps commission type id to CommissionType object.

################################################################################
    def __getitem__(self, key: int) -> Optional[TCommissionType]:

        try:
            return self._types[key]
        except IndexError:
            return None

################################################################################
    def __contains__(self, key: int) -> bool:

        return key in self._types

################################################################################
    @property
    def types(self) -> List[TCommissionType]:

        return [t for t in self._types.values()]

################################################################################
    def load_type(self, data: Tuple[int, str, int, Optional[str], Optional[str]]) -> None:

        self._types[data[0]] = TCommissionType.load(self, data)

################################################################################
    def status(self) -> Embed:

        fields = [
            EmbedField(
                name=f"{_type.name} ({_type.id})",
                value=(
                    f"**Price:** {_type.price}\n"
                    f"**Description:** {_type.description}"
                ),
                inline=False
            )
            for _type in self._types.values()
        ]

        return make_embed(
            title="Commission Types Overview",
            description=(
                f"**{len(self._types)}** commission types registered.\n\n"
                
                "Please select a commission type from the\n"
                "selector below to view and edit its details.\n"
                f"{draw_separator(extra=26)}"
            ),
            fields=fields,
        )

################################################################################
    def match_type(self, name: str, price: int, description: Optional[str]) -> Optional[TCommissionType]:

        for _type in self._types.values():
            if _type.name == name and _type.price == price:
                if description is None:
                    return _type
                elif _type.description == description:
                    return _type
                elif fuzzy_match(description, _type.description) > 80:
                    return _type

################################################################################
    async def main_menu(self, interaction: Interaction) -> None:

        status = self.status()

        await interaction.response.send_message(embed=status)

################################################################################
    async def add_type(self, interaction: Interaction) -> None:

        modal = CommissionTypeModal()

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        name, price, description = modal.value
        new_type = TCommissionType.new(self, name, price, description)

        self._types[name] = new_type

        # Emulate the Type main menu since we need to do a followup here
        # instead of an initial response.
        embed = new_type.status()
        view = CommissionTypeStatusView(interaction.user, new_type)

        await interaction.followup.send(embed=embed, view=view)
        await view.wait()

        return

################################################################################
    @staticmethod
    async def edit_type(interaction: Interaction, comm_type: TCommissionType) -> None:

        status = comm_type.status()
        view = CommissionTypeStatusView(interaction.user, comm_type)

        await interaction.response.send_message(embed=status, view=view)
        await view.wait()

        return

################################################################################
    async def status_all(self, interaction: Interaction) -> None:

        await interaction.response.send_message(embed=self.status())

################################################################################
    async def remove_type(self, interaction: Interaction, type_id: int) -> None:

        c = db_connection.cursor()
        c.execute(
            "DELETE FROM commission_types WHERE type_id = %s",
            (type_id,)
        )

        db_connection.commit()
        c.close()

        complete = make_embed(
            title="Commission Type Removed",
            description=(
                f"Commission type __**{self[type_id].name}**__ has been removed.\n"
                f"{draw_separator(extra=25)}"
            )
        )
        view = CloseMessageView(interaction.user)

        # Delete it here, so we can still reference it in the confirmation message.
        self.types.remove(self[type_id])

        await interaction.followup.send(embed=complete, view=view)
        await view.wait()

        return

################################################################################
