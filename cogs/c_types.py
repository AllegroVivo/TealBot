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
        name="comm_types",
        description="Commission type-related commands."
    )

################################################################################
    @comm_types.command(
        name="add",
        description="Add a new commission type."
    )
    async def types_add(self, ctx: ApplicationContext) -> None:

        await self.bot.type_manager.add_type(ctx.interaction)

################################################################################
    @comm_types.command(
        name="edit",
        description="View and edit a commission type."
    )
    async def types_edit(
        self,
        ctx: ApplicationContext,
        type_id: Option(
            SlashCommandOptionType.integer,
            name="type_id",
            description="The ID of the commission type to edit.",
            required=True
        )
    ) -> None:

        tm = self.bot.type_manager

        try:
            comm_type = tm[type_id]
        except IndexError:
            error = TypeNotFoundError(type_id)
            await ctx.respond(embed=error, ephemeral=True)
            return

        await self.bot.type_manager.edit_type(ctx.interaction, comm_type)

################################################################################
    @comm_types.command(
        name="add_image",
        description="Add an image to a commission type."
    )
    async def types_add_image(
        self,
        ctx: ApplicationContext,
        type_id: Option(
            SlashCommandOptionType.integer,
            name="type_id",
            description="The ID of the commission type to edit.",
            required=True
        ),
        image: Option(
            SlashCommandOptionType.attachment,
            name="image",
            description="The image to add.",
            required=True
        )
    ) -> None:

        tm = self.bot.type_manager
        comm_type = tm[type_id]

        if comm_type is None:
            error = TypeNotFoundError(type_id)
            await ctx.respond(embed=error, ephemeral=True)
            return

        await comm_type.add_image(ctx.interaction, image)

################################################################################
def setup(bot: "TealBot") -> None:

    bot.add_cog(CommTypes(bot))

################################################################################
