from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from discord import Embed, EmbedField, User
from typing import TYPE_CHECKING, List, Optional, Type, TypeVar

from utilities import *

if TYPE_CHECKING:
    from .client import TClient
################################################################################

__all__ = (
    "TCommission",
    "TCommissionItem",
)

TC = TypeVar("TC", bound="TCommission")

################################################################################
@dataclass
class TCommissionItem:

    _type: CommissionType
    _qty: int
    _completed: bool

################################################################################
    def __eq__(self, other: TCommissionItem) -> bool:

        return (
            self._type == other._type
            and self._qty == other._qty

            # Not sure if we should compare completion status.
            # Let's not for now.
            # and self._completed == other._completed
        )

################################################################################
class TCommission:

    __slots__ = (
        "_client",
        "_id",
        "_items",
        "_price",
        "_tags",
        "_description",
        "_notes",
        "_create_date",
        "_start_date",
        "_deadline",
        "_status",  # Will include "Completed" so we don't need to duplicate that below.
        "_paid",
        "_paid_date",
        "_update_date",
        "_complete_date",
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
        description: Optional[str],
        notes: Optional[str],
        status: CommissionStatus,
        paid: bool,
        vip: bool,
        rush: bool,
        create_date: datetime,
        update_date: datetime,
        start_date: Optional[datetime],
        deadline: Optional[datetime],
        paid_date: Optional[datetime],
        complete_date: Optional[datetime]
    ):

        self._id: str = _id
        self._client: TClient = client
        self._items: List[TCommissionItem] = items
        self._tags: List[CommissionTag] = tags

        self._price: int = price
        self._description: Optional[str] = description
        self._notes: Optional[str] = notes

        self._status: CommissionStatus = status
        self._paid: bool = paid
        self._vip: bool = vip
        self._rush: bool = rush

        self._create_date: datetime = create_date
        self._update_date: datetime = update_date
        self._start_date: Optional[datetime] = start_date
        self._deadline: Optional[datetime] = deadline
        self._paid_date: Optional[datetime] = paid_date
        self._complete_date: Optional[datetime] = complete_date

################################################################################
    @classmethod
    def new(
        cls: Type[TC],
        user: User,
        item: str,
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

        pass

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
    def description(self) -> Optional[str]:

        return self._description

################################################################################
    @property
    def notes(self) -> Optional[str]:

        return self._notes

################################################################################
    @property
    def status(self) -> CommissionStatus:

        return self._status

################################################################################
    @property
    def paid(self) -> bool:

        return self._paid

################################################################################
    @property
    def start_date(self) -> datetime:

        return self._start_date

################################################################################
    @property
    def deadline(self) -> datetime:

        return self._deadline

################################################################################
    @property
    def paid_date(self) -> Optional[datetime]:

        return self._paid_date

################################################################################
    @property
    def update_date(self) -> datetime:

        return self._update_date

################################################################################
    @property
    def complete_date(self) -> Optional[datetime]:

        return self._complete_date

################################################################################
    @property
    def vip(self) -> bool:

        return self._vip

################################################################################
    @property
    def rush(self) -> bool:

        return self._rush

################################################################################
    @property
    def in_progress(self) -> bool:

        return self._complete_date is None

################################################################################
    def offer_to_merge(
        self,
        comm: TCommission,
        item: str,
        qty: int,
        vip: bool,
        rush: bool,
        price: Optional[int]
    ) -> bool:

        pass

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
