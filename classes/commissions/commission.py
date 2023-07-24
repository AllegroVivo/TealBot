from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from discord import Embed, EmbedField, User
from typing import TYPE_CHECKING, List, Optional, Type, TypeVar

from assets import BotEmojis
from .dates import TCommissionDates
from utilities import *

if TYPE_CHECKING:
    from .client import TClient
    from .item import TCommissionItem
################################################################################

__all__ = (
    "TCommission",
)

TC = TypeVar("TC", bound="TCommission")

################################################################################
class TCommission:

    __slots__ = (
        "_client",
        "_id",
        "_items",
        "_price",
        "_tags",
        "_notes",
        "_dates",
        "_status",  # Will include "Completed" so we don't need to duplicate that below.
        "_paid",
        "_vip",
        "_rush",
    )

################################################################################
    def __init__(
        self,
        _id: str,
        client: TClient,
        items: List[TCommissionItem],
        tags: List[CommissionTag],
        price: int,
        notes: Optional[str],
        status: CommissionStatus,
        paid: bool,
        vip: bool,
        rush: bool,
        create_date: datetime
    ):

        self._id: str = _id
        self._client: TClient = client

        self._details: TCommissionDetails = TCommissionDetails(self, items, tags, price, notes)
        self._dates: TCommissionDates = TCommissionDates(self, create_date)

################################################################################
    @classmethod
    def new(
        cls: Type[TC],
        user: User,
        item: int,
        qty: int,
        vip: bool,
        rush: bool,
        price: Optional[int],
    ) -> TC:

        # Make TClient object here

        return cls(
            _id=...,
            client=None,
            items=[],
            tags=[],
            price=0,
            description=None,
            notes=None,
            status=CommissionStatus.Pending,
            paid=False,
            vip=False,
            rush=False,
            create_date=datetime.now(),
            update_date=datetime.now(),
            start_date=None,
            deadline=None,
            paid_date=None,
            complete_date=None
        )

################################################################################
    def status(self) -> Embed:

        vip_emoji = BotEmojis.Check if self._vip else BotEmojis.Cross
        rush_emoji = BotEmojis.Check if self._rush else BotEmojis.Cross

        paid_emote = BotEmojis.Check if self._paid else BotEmojis.Cross
        paid_text = "Paid" if self._paid else "Unpaid"
        price_field = (
            f"{paid_emote} - `{self.price}`\n"
            f"*({paid_text})*"
        )

        fields = [
            EmbedField(name="__Client__", value=self.client.mention, inline=True),
            EmbedField(name="__VIP Comm__", value=vip_emoji, inline=True),
            EmbedField(name="__Rush Comm__", value=rush_emoji, inline=True),

            EmbedField(name="__Commission Items__", value="`Placeholder~`", inline=True),
            EmbedField(name="__Price__", value=price_field, inline=True),

            EmbedField(name="__Current Status__", value=f"`{self._status.name}`", inline=True),


        ]

################################################################################
    @property
    def id(self) -> str:

        return self._id

################################################################################
    @property
    def client(self) -> TClient:

        return self._client

################################################################################
    @property
    def items(self) -> List[TCommissionItem]:

        return self._items

################################################################################
    @property
    def tags(self) -> List[CommissionTag]:

        return self._tags

################################################################################
    @property
    def price(self) -> int:

        return self._price

################################################################################
    @property
    def notes(self) -> Optional[str]:

        return self._notes

################################################################################
    @property
    def commission_status(self) -> CommissionStatus:

        return self._status

################################################################################
    @property
    def paid(self) -> bool:

        return self._paid

################################################################################
    @property
    def vip(self) -> bool:

        return self._vip

################################################################################
    @property
    def rush(self) -> bool:

        return self._rush

################################################################################
    def update(self) -> None:

        c = db_connection.cursor()
        c.execute(
            "UPDATE commissions SET items = %s, tags = %s, price = %s, "
            "description = %s, notes = %s, status = %s, paid = %s, "
            "start_date = %s, deadline = %s, paid_date = %s, update_date = %s, "
            "complete_date = %s, vip = %s, rush = %s WHERE commission_id = %s",
            (
                self._items, self._tags, self._price, self._description,
                self._notes, self._status, self._paid, self._start_date,
                self._deadline, self._paid_date, self._update_date,
                self._complete_date, self._vip, self._rush, self._id.hex
            )
        )

        db_connection.commit()
        c.close()

################################################################################
