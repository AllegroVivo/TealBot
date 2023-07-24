from discord        import (
    ApplicationContext,
    Cog,
    Option,
    OptionChoice,
    SlashCommandGroup,
    SlashCommandOptionType,
    slash_command
)
from typing         import TYPE_CHECKING

from utilities      import *

if TYPE_CHECKING:
    from classes.bot import TealBot
################################################################################
class CommTypes(Cog):

    def __init__(self, bot: "TealBot"):

        self.bot: "TealBot" = bot

################################################################################

    comm_types = SlashCommandGroup(
        name="types",
        description="Commission type-related commands."
    )

################################################################################
    @comm_types.command(
        name="add",
        description="Add a new commission type."
    )
    async def types_add(self, ctx: ApplicationContext):

        await self.bot.commission_manager.add_type(ctx.interaction)

################################################################################
def setup(bot: "TealBot") -> None:

    bot.add_cog(CommTypes(bot))

################################################################################
