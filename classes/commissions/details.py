from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Type, TypeVar

from utilities import *

if TYPE_CHECKING:
    from .commission import TCommission
    from .item import TCommissionItem
################################################################################

__all__ = (
    "TCommissionDetails",
)

CD = TypeVar("CD", bound="TCommissionDetails")

################################################################################
class TCommissionDetails:

    __slots__ = (
        "_parent",
        "_items",
        "_tags",
        "_status",
        "_notes",
        "_price",
        "_paid",
        "_vip",
        "_rush",
    )

################################################################################
    def __init__(
        self,
        parent: TCommission,
        items: List[TCommissionItem],
        tags: List[CommissionTag],
        status: CommissionStatus,
        notes: Optional[str],
        price: int,
        paid: bool,
        vip: bool,
        rush: bool
    ):

        self._parent: TCommission = parent

        self._items: List[TCommissionItem] = items
        self._tags: List[CommissionTag] = tags

        self._status: CommissionStatus = status
        self._notes: Optional[str] = notes

        self._price: int = price
        self._paid: bool = paid

        self._vip: bool = vip
        self._rush: bool = rush

################################################################################
    @classmethod
    def new(
        cls: Type[CD],
        parent: TCommission,
        items: List[TCommissionItem],
        price: int,
        vip: bool,
        rush: bool
    ) -> CD:

        return cls(
            parent,
            items,
            [],  # No tags yet.
            CommissionStatus.Pending,  # No status yet.
            None,  # No notes yet.
            price,
            False,  # Not paid yet.
            vip,
            rush
        )

################################################################################
