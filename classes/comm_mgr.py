from __future__ import annotations

from discord import ApplicationContext, User
from typing import TYPE_CHECKING, List, Optional

from utilities import *

if TYPE_CHECKING:
    from .bot import TealBot
    from .commission import TCommission
################################################################################

__all__ = (
    "CommissionManager",
)

################################################################################
class CommissionManager:

    __slots__ = (
        "_parent",
        "_commissions"
    )

################################################################################
    def __init__(self, parent: TealBot):

        self._parent: TealBot = parent
        self._commissions: List[TCommission] = []

################################################################################
    def add_commission(
        self,
        ctx: ApplicationContext,
        user: User,
        item: str,
        qty: int,
        vip: bool,
        rush: bool,
        price: Optional[int],
    ) -> None:

        pass

################################################################################
    def _get_commission_raw(
        self,
        ctx: ApplicationContext,
        user: User,
        item: str,
        qty: int,
        vip: bool,
        rush: bool,
        price: Optional[int],
    ) -> None:
################################################################################
