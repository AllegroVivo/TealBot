from __future__ import annotations

from discord    import Bot
from typing     import TYPE_CHECKING, List

from classes.commissions.comm_mgr import TCommissionManager
from classes.config import TConfiguration
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
        "_t_guilds",
        "_commission_manager",
        "_client_manager",
        "_type_manager",
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._t_guilds: List[TConfiguration] = []

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
    async def load_configurations(self) -> None:

        c = db_connection.cursor()
        c.execute("SELECT * FROM config")
        data = c.fetchall()
        c.close()

        for guild_record in data:
            guild = self.get_guild(guild_record[0])
            if guild is None:
                continue

            config = TConfiguration(guild)
            await config.load_channels(guild_record[1:])
            self._t_guilds.append(config)

################################################################################
    async def load_clients(self) -> None:

        c = db_connection.cursor()
        c.execute("SELECT * FROM clients")
        data = c.fetchall()

        for record in data:
            user = await self.get_or_fetch_user(record[0]) or record[0]
            self.client_manager.load_client(user, record[1:])

################################################################################
    async def load_types(self) -> None:

        c = db_connection.cursor()
        c.execute("SELECT * FROM commission_types")
        data = c.fetchall()

        for record in data:
            self.type_manager.load_type(record)

################################################################################
