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
class Clients(Cog):

    def __init__(self, bot: "TealBot"):

        self.bot: "TealBot" = bot

################################################################################

    clients = SlashCommandGroup(
        name="clients",
        description="Client-related commands."
    )

################################################################################
    @clients.command(
        name="add",
        description="Add a new client."
    )
    async def clients_add(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="A Discord mention of the new client.",
            required=True
        )
    ):

        cm = self.bot.client_manager
        client = cm[user.id]
        if client is not None:
            error = ClientAlreadyExistsError(user)
            await ctx.respond(embed=error, ephemeral=True)
            return

        client = await cm.add_client(ctx.interaction, user)
        await client.main_menu(ctx.interaction)

################################################################################
    @clients.command(
        name="status",
        description="View and edit a client's record."
    )
    async def clients_status(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="A Discord mention of the client.",
            required=True
        )
    ) -> None:

        cm = self.bot.client_manager

        client = cm[user.id]
        if client is None:
            client = await cm.add_client(ctx.interaction, user)

        await client.main_menu(ctx.interaction)

################################################################################
def setup(bot: "TealBot") -> None:

    bot.add_cog(Clients(bot))

################################################################################
