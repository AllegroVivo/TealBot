from __future__ import annotations

from datetime import datetime
from discord import User
from typing import TYPE_CHECKING, List, Optional

from .commission import TCommission

if TYPE_CHECKING:
    pass
################################################################################

__all__ = (
    "TClient",
)

################################################################################
class TClient:

    __slots__ = (
        "_user",
        "_name",
        "_communication_method",
        "_commissions",
        "_tags",
        "_notes",
        "_update_date",
        "_email",
        "_paypal",
    )

################################################################################
    def __init__(self):

        self._user: User = None  # type: ignore
        self._commissions: List[TCommission] = []

        self._name: str = None  # type: ignore
        self._notes: Optional[str] = None
        self._tags: List[ClientTag] = []

        self._update_date: Optional[datetime] = None
        self._communication_method: Optional[CommunicationMethod] = None
        self._email: Optional[str] = None
        self._paypal: Optional[str] = None

################################################################################
