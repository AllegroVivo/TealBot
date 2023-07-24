from __future__ import annotations

from discord import Cog
from typing import TYPE_CHECKING
from utilities import assert_db_structure

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

        print("Loading Client data...")
        await self.bot.load_clients()

        # print("Loading commission data...")
        # await self.bot.load_commissions()

        print("TealBot Online!")

################################################################################
def setup(bot: TealBot) -> None:

    bot.add_cog(Internal(bot))

################################################################################
