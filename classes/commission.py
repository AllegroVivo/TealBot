from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from utilities import *

if TYPE_CHECKING:
    pass
################################################################################

__all__ = (
    "TCommission",
    "TCommissionItem",
)

################################################################################
@dataclass
class TCommissionItem:

    _type: CommissionType
    _qty: int
    _completed: bool

################################################################################
class TCommission:

    __slots__ = (
        "_client",
        "_items",
        "_price",
        "_tags",
        "_description",
        "_notes",
        "_start_date",
        "_deadline",
        "_status",  # Will include "Completed" so we don't need to duplicate that below.
        "_paid",
        "_paid_date",
        "_update_date",
        "_complete_date",
    )

################################################################################
    def __init__(self):

        self._client: TClient = None
        self._items: List[TCommissionItem] = []
        self._tags: List[CommissionTag] = []

        self._price: int = 0
        self._description: Optional[str] = None
        self._notes: Optional[str] = None

        self._status: CommissionStatus = CommissionStatus.Pending
        self._paid: bool = False

        self._start_date: Optional[datetime] = None
        self._deadline: Optional[datetime] = None
        self._paid_date: Optional[datetime] = None
        self._update_date: Optional[datetime] = None
        self._complete_date: Optional[datetime] = None


################################################################################
