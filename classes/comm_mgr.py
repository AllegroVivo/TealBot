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
    @property
    def bot(self) -> TealBot:

        return self._parent

################################################################################
    @property
    def commissions(self) -> List[TCommission]:

        return self._commissions

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

        comm = self._get_commission_raw(ctx, user, item, qty, vip, rush, price)
        if comm is not None:
            raise ValueError("Possible duplicate commission already exists.")

        commission = TCommission(

        )

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
    ) -> Optional[TCommission]:

        # Compare to all open commissions and see if we can find a match.
        return

################################################################################
    @property
    def open_commissions(self) -> List[TCommission]:

        return [c for c in self._commissions if c.in_progress]

################################################################################
