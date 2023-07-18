from __future__ import annotations

from discord import Interaction, User
from typing import TYPE_CHECKING, List, Optional

from utilities import *

if TYPE_CHECKING:
    from .bot import TealBot
    from .commission import TCommission
    from .client import TClient
################################################################################

__all__ = (
    "CommissionManager",
)

################################################################################
class CommissionManager:

    __slots__ = (
        "_parent",
        "_commissions",
        "_clients",
    )

################################################################################
    def __init__(self, parent: TealBot):

        self._parent: TealBot = parent
        self._commissions: List[TCommission] = []
        self._clients: List[TClient] = []

################################################################################
    @property
    def bot(self) -> TealBot:

        return self._parent

################################################################################
    @property
    def commissions(self) -> List[TCommission]:

        return self._commissions

################################################################################
    @property
    def clients(self) -> List[TClient]:

        return self._clients

################################################################################
    def add_commission(
        self,
        interaction: Interaction,
        user: User,
        item: str,
        qty: int,
        vip: bool,
        rush: bool,
        price: Optional[int],
    ) -> None:

        for comm in self._commissions:
            if comm.client == user:
                comm.offer_to_merge(comm, item, qty, vip, rush, price)
                return

        new_comm = TCommission.new(user, item, qty, vip, rush, price)
        confirm = self.confirm_new_commission(new_comm)
        if confirm:
            self._commissions.append(new_comm)

################################################################################
    @property
    def open_commissions(self) -> List[TCommission]:

        return [c for c in self._commissions if c.in_progress]

################################################################################
