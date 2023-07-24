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
class Commissions(Cog):

    def __init__(self, bot: "TealBot"):

        self.bot: "TealBot" = bot

################################################################################

    commissions = SlashCommandGroup(
        name="commissions",
        description="Commission-related commands."
    )

################################################################################
    # @commissions.command(
    #     name="add_commission",
    #     description="View and update name, custom URL, jobs, accent color, & rates."
    # )
    # async def commissions_add(
    #     self,
    #     ctx: ApplicationContext,
    #     member: Option(
    #         SlashCommandOptionType.user,
    #         name="user",
    #         description="The user to add a commission for.",
    #         required=True
    #     ),
    #     item: Option(
    #         SlashCommandOptionType.string,
    #         name="item",
    #         description="The item being commissioned.",
    #         required=True,
    #         choices=[
    #             OptionChoice("Chibi", "1"),
    #             OptionChoice("Chibify", "2"),
    #             OptionChoice("Emote", "3"),
    #             OptionChoice("Sticker", "4"),
    #             OptionChoice("Twitch Panel", "5"),
    #             OptionChoice("Twitch Sub Badge", "6"),
    #             OptionChoice("Twitch Sub Flair", "7"),
    #             OptionChoice("Twitch Scene", "8"),
    #             OptionChoice("Avatar", "9"),
    #             OptionChoice("Other", "10")
    #         ]
    #     ),
    #     qty: Option(
    #         SlashCommandOptionType.integer,
    #         name="quantity",
    #         description="The number of items being commissioned.",
    #         required=True
    #     ),
    #     vip: Option(
    #         SlashCommandOptionType.boolean,
    #         name="vip",
    #         description="Whether or not this commission is a VIP order.",
    #         required=False,
    #         default=False
    #     ),
    #     rush: Option(
    #         SlashCommandOptionType.boolean,
    #         name="rush",
    #         description="Whether or not this commission is a rush order.",
    #         required=False,
    #         default=False
    #     ),
    #     price: Option(
    #         SlashCommandOptionType.integer,
    #         name="price_override",
    #         description="The price of the commission, if different from the default.",
    #         required=False
    #     ),
    # ) -> None:
    #
    #     self.bot.commission_manager.add_commission(
    #         ctx.interaction,
    #         member,
    #         int(item),
    #         qty,
    #         vip,
    #         rush,
    #         price
    #     )

################################################################################
    @commissions.command(
        name="add",
        description="Add a new commission type."
    )
    async def commissions_add_type(
        self,
        ctx: ApplicationContext,
        name: Option(
            SlashCommandOptionType.string,
            name="name",
            description="The name of the new commission type.",
            required=True
        ),
        price: Option(
            SlashCommandOptionType.integer,
            name="price",
            description="The price of the new commission type.",
            required=True
        ),
        description: Option(
            SlashCommandOptionType.string,
            name="description",
            description="The description of the new commission type if applicable.",
            required=False
        )
    ):

        cm = self.bot.commission_manager
        await cm.add_type(ctx.interaction, name, price, description)

################################################################################
def setup(bot: "TealBot") -> None:

    bot.add_cog(Commissions(bot))

################################################################################
