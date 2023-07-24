from __future__ import annotations

from discord import Interaction, User
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

from ui import ConfirmCancelView, CloseMessageView, ClientStatusView
from utilities import *

if TYPE_CHECKING:
    from classes.bot import TealBot
    from .commission import TCommission
    from .client import TClient
    from .comm_type import TCommissionType
################################################################################

__all__ = (
    "TCommissionManager",
)

################################################################################
class TCommissionManager:

    __slots__ = (
        "_parent",
        "_commissions",
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
