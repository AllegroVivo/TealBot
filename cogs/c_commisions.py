from discord        import (
    ApplicationContext,
    Cog,
    Option,
    OptionChoice,
    SlashCommandGroup,
    SlashCommandOptionType,
)
from typing         import TYPE_CHECKING

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
    @commissions.command(
        name="add",
        description="View and update name, custom URL, jobs, accent color, & rates."
    )
    async def commissions_add(
        self,
        ctx: ApplicationContext,
        member: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user to add a commission for.",
            required=True
        ),
        item: Option(
            SlashCommandOptionType.string,
            name="item",
            description="The item being commissioned.",
            required=True,
            choices=[
                OptionChoice("Chibi", "chibi"),
                OptionChoice("Chibify", "chibify"),
                OptionChoice("Emote", "emote"),
                OptionChoice("Sticker", "sticker"),
                OptionChoice("Twitch Panel", "panel"),
                OptionChoice("Twitch Sub Badge", "subbadge"),
                OptionChoice("Twitch Sub Flair", "subflair"),
                OptionChoice("Twitch Scene", "scene"),
                OptionChoice("Avatar", "avatar"),
            ]
        ),
        qty: Option(
            SlashCommandOptionType.integer,
            name="quantity",
            description="The number of items being commissioned.",
            required=True
        ),
        vip: Option(
            SlashCommandOptionType.boolean,
            name="vip",
            description="Whether or not this commission is a VIP order.",
            required=False,
            default=False
        ),
        rush: Option(
            SlashCommandOptionType.boolean,
            name="rush",
            description="Whether or not this commission is a rush order.",
            required=False,
            default=False
        ),
        price: Option(
            SlashCommandOptionType.integer,
            name="price_override",
            description="The price of the commission, if different from the default.",
            required=False
        ),
    ) -> None:

        self.bot.commission_manager.add_commission(
            ctx,
            member,
            item,
            qty,
            vip,
            rush,
            price
        )

################################################################################
def setup(bot: "TealBot") -> None:

    bot.add_cog(Commissions(bot))

################################################################################
