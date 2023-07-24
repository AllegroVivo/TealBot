from __future__ import annotations

from discord import Attachment, Embed, EmbedField, Interaction
from discord.ext.pages import Page
from typing import TYPE_CHECKING, Dict, Optional, Tuple, Type, TypeVar

from ui.common import *
from ui.types import *
from utilities import *

from assets import BotEmojis

if TYPE_CHECKING:
    from classes.commissions import TCommissionTypeManager
################################################################################

__all__ = (
    "TCommissionType",
)

CT = TypeVar("CT", bound="TCommissionType")

################################################################################
class TCommissionType:

    __slots__ = (
        "_parent",
        "_id",
        "_name",
        "_price",
        "_description",
        "_image",
    )

################################################################################
    def __init__(
        self,
        parent: TCommissionTypeManager,
        _id: int,
        name: str,
        price: int,
        description: Optional[str],
        image: Optional[str] = None
    ):

        self._parent: TCommissionTypeManager = parent

        self._id: int = _id
        self._name: str = name
        self._price: int = price

        self._description: Optional[str] = description
        self._image: Optional[str] = image

################################################################################
    @classmethod
    def new(
        cls: Type[CT],
        parent: TCommissionTypeManager,
        name: str,
        price: int,
        description: Optional[str]
    ) -> CT:

        type_id = new_commission_type(name, price, description)

        return cls(
            parent=parent,
            _id=type_id,
            name=name,
            price=price,
            description=description,
            image=None
        )

################################################################################
    @classmethod
    def load(
        cls: Type[CT],
        parent: TCommissionTypeManager,
        data: Tuple[int, str, int, Optional[str], Optional[str]]
    ) -> CT:

        return cls(
            parent=parent,
            _id=data[0],
            name=data[1],
            price=data[3],
            description=data[2],
            image=data[4]
        )

################################################################################
    def __eq__(self, other: TCommissionType) -> bool:

        return self.id == other.id

################################################################################
    @property
    def parent(self) -> TCommissionTypeManager:

        return self._parent

################################################################################
    @property
    def id(self) -> int:

        return self._id

################################################################################
    @property
    def name(self) -> str:

        return self._name

################################################################################
    @property
    def price(self) -> int:

        return self._price

################################################################################
    @property
    def description(self) -> Optional[str]:

        return self._description

################################################################################
    @property
    def image(self) -> Optional[str]:

        return self._image or Embed.Empty

################################################################################
    def status(self) -> Embed:

        description = (
            f"**Price:** {self.price}\n"
            f"{draw_separator(extra=6)}\n"
        )
        description += (
            f"**Description:** {self.description}\n"
            f"{draw_separator(text=f'**Description:** {self.description}', extra=-2)}\n"
        ) if self.description is not None else ""

        return make_embed(
            title=f"{BotEmojis.TealLogo} {self.name}",
            description=description,
            footer_text=f"(ID: {self.id})",
            thumbnail_url=self.image
        )

################################################################################
    async def set_values(self, interaction: Interaction) -> None:

        modal = CommissionTypeModal(self.name, self.price, self.description)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        name, price, description = modal.value
        self.update(name, price, description, self._image)

        return

################################################################################
    async def add_image(self, interaction: Interaction, image: Attachment) -> None:

        pass

################################################################################
    async def remove(self, interaction: Interaction) -> None:

        confirm = make_embed(
            title="Confirm Removal",
            description=(
                f"Are you sure you want to remove the commission type "
                f"__**{self.name}**__?\n"
                f"{draw_separator(extra=20)}"
            ),
            footer_text=f"(Type ID: -{self.id}-)"
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.response.send_message(embed=confirm, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        # We need to pass control back to the parent to remove the type
        # from the database and the manager.
        await self.parent.remove_type(interaction, self.id)

################################################################################
    def update(
        self,
        name: str,
        price: int,
        description: Optional[str],
        image: Optional[str]
    ) -> None:

        # We're doing the update method differently here because three values
        # (name, price, description) are being set all at once, and we don't want
        # to have to make three separate calls to the database. So we're going to
        # do it all in one go.

        self._name = name
        self._price = price
        self._description = description
        self._image = image

        c = db_connection.cursor()
        c.execute(
            "UPDATE commission_types SET name = %s, description = %s, price = %s, "
            "image = %s WHERE type_id = %s",
            (self.name, self.description, self.price, self._image, self.id)
        )

        db_connection.commit()
        c.close()

        return

################################################################################
