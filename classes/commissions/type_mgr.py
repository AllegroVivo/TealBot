from __future__ import annotations

from discord import Embed, EmbedField, Interaction
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Type, TypeVar

from .type import TCommissionType
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
        self._types: Dict[str, TCommissionType] = {}  # Maps commission type name to CommissionType object.

################################################################################
    def __getitem__(self, key: str) -> Optional[TCommissionType]:

        try:
            return self._types[key]
        except IndexError:
            return None

################################################################################
    def __contains__(self, key: str) -> bool:

        return key in self._types

################################################################################
    @property
    def types(self) -> List[TCommissionType]:

        return [t for t in self._types.values()]

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
    def add_type(self, name: str, price: int, description: Optional[str]) -> None:

        self._types[name] = TCommissionType.new(name, price, description)

################################################################################
