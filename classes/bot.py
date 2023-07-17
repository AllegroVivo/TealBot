from __future__ import annotations

from discord    import Bot
from typing     import TYPE_CHECKING

from .comm_mgr import CommissionManager

if TYPE_CHECKING:
    pass
################################################################################

__all__ = (
    "TealBot",
)

################################################################################
class TealBot(Bot):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._commission_manager: CommissionManager = CommissionManager(self)

################################################################################
