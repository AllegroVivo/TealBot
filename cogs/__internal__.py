from __future__ import annotations

from discord import Cog, Guild
from typing import TYPE_CHECKING
from utilities import assert_db_structure, assert_guild_records

if TYPE_CHECKING:
    from classes.bot import TealBot
################################################################################
class Internal(Cog):

    def __init__(self, bot: TealBot):

        self.bot: TealBot = bot

################################################################################
    @Cog.listener("on_ready")
    async def on_ready(self) -> None:

        print("Asserting database structure...")
        assert_db_structure()
        assert_guild_records(self.bot.guilds)

        print("Loading guild configurations...")
        await self.bot.load_configurations()

        print("Loading commission type data...")
        await self.bot.load_types()

        print("Loading client data...")
        await self.bot.load_clients()

        # print("Loading commission data...")
        # await self.bot.load_commissions()

        print("TealBot Online!")

################################################################################
    @Cog.listener("on_guild_join")
    async def on_guild_join(self, guild: Guild) -> None:

        assert_guild_records([guild])

################################################################################
def setup(bot: TealBot) -> None:

    bot.add_cog(Internal(bot))

################################################################################
