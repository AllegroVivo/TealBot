from __future__ import annotations

from discord    import Bot
from typing     import TYPE_CHECKING

from classes.commissions.comm_mgr import TCommissionManager
from classes.commissions.client_mgr import TClientManager
from classes.commissions.type_mgr import TCommissionTypeManager
from utilities import db_connection

if TYPE_CHECKING:
    pass
################################################################################

__all__ = (
    "TealBot",
)

################################################################################
class TealBot(Bot):

    __slots__ = (
        "_commission_manager",
        "_client_manager",
        "_type_manager",
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._commission_manager: TCommissionManager = TCommissionManager(self)
        self._client_manager: TClientManager = TClientManager(self)
        self._type_manager: TCommissionTypeManager = TCommissionTypeManager(self)

################################################################################
    @property
    def commission_manager(self) -> TCommissionManager:

        return self._commission_manager

################################################################################
    @property
    def client_manager(self) -> TClientManager:

        return self._client_manager

################################################################################
    @property
    def type_manager(self) -> TCommissionTypeManager:

        return self._type_manager

################################################################################
    async def load_clients(self) -> None:

        c = db_connection.cursor()
        c.execute("SELECT * FROM clients")
        data = c.fetchall()

        for record in data:
            user = await self.get_or_fetch_user(record[0]) or record[0]
            self.commission_manager._load_client(user, record[1:])

################################################################################
