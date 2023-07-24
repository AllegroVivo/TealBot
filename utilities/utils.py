from __future__ import annotations

import math
import re

from datetime       import datetime
from discord import Colour, Embed, EmbedField, Interaction
from discord.embeds import EmptyEmbed
from rapidfuzz      import fuzz
from typing         import TYPE_CHECKING, Any, List, Literal, Optional, Tuple, Union

from assets import BotImages

if TYPE_CHECKING:
    pass
################################################################################

__all__ = (
    "make_embed",
    "draw_separator",
    "titleize",
    "fuzzy_match",
    "NS",
    "format_timestamp",
    "edit_message_helper",
)

################################################################################
def make_embed(
    *,
    title: str = EmptyEmbed,
    description: str = EmptyEmbed,
    url: str = EmptyEmbed,
    color: Optional[Union[Colour, int]] = None,
    thumbnail_url: str = EmptyEmbed,
    image_url: str = EmptyEmbed,
    author_text: str = EmptyEmbed,
    author_url: str = EmptyEmbed,
    author_icon: str = EmptyEmbed,
    footer_text: str = EmptyEmbed,
    footer_icon: str = EmptyEmbed,
    timestamp: Union[datetime, bool] = False,
    fields: Optional[List[Union[Tuple[str, Any, bool], EmbedField]]] = None
) -> Embed:

    embed = Embed(
        colour=color or Colour.teal(),
        title=title,
        description=description,
        url=url
    )

    embed.set_thumbnail(url=thumbnail_url)
    embed.set_image(url=image_url)

    if author_text is not EmptyEmbed:
        embed.set_author(
            name=author_text,
            url=author_url,
            icon_url=author_icon
        )
    # else:
    #     embed.set_author(
    #         name="*•.¸♡ Teal Creations ♡¸.•*",
    #         url="https://tealcreations.art/",
    #         icon_url=BotImages.TealLogo
    #     )

    if footer_text is not EmptyEmbed:
        embed.set_footer(
            text=footer_text,
            icon_url=footer_icon
        )

    if isinstance(timestamp, datetime):
        embed.timestamp = timestamp
    elif timestamp is True:
        embed.timestamp = datetime.now()

    if fields is not None:
        if all(isinstance(f, EmbedField) for f in fields):
            embed.fields = fields
        else:
            for f in fields:
                if isinstance(f, EmbedField):
                    embed.fields.append(f)
                elif isinstance(f, tuple):
                    embed.add_field(name=f[0], value=f[1], inline=f[2])
                else:
                    continue

    return embed

################################################################################
def draw_separator(*, text: str = "", num_emoji: int = 0, extra: float = 0.0) -> str:

    text_value = extra + (1.95 * num_emoji)

    for c in text:
        if c == "'":
            text_value += 0.25
        elif c in ("i", "j", ".", " "):
            text_value += 0.30
        elif c in ("I", "!", ";", "|", ","):
            text_value += 0.35
        elif c in ("f", "l", "`", "[", "]"):
            text_value += 0.40
        elif c in ("(", ")", "t"):
            text_value += 0.45
        elif c in ("r", "t", "1" "{", "}", '"', "\\", "/"):
            text_value += 0.50
        elif c in ("s", "z", "*", "-"):
            text_value += 0.60
        elif c in ("x", "^"):
            text_value += 0.65
        elif c in ("a", "c", "e", "g", "k", "v", "y", "J", "7", "_", "=", "+", "~", "<", ">", "?"):
            text_value += 0.70
        elif c in ("n", "o", "u", "2", "5", "6", "8", "9"):
            text_value += 0.75
        elif c in ("b", "d", "h", "p", "q", "E", "F", "L", "S", "T", "Z", "3", "4", "$"):
            text_value += 0.80
        elif c in ("P", "V", "X", "Y", "0"):
            text_value += 0.85
        elif c in ("A", "B", "C", "D", "K", "R", "#", "&"):
            text_value += 0.90
        elif c in ("G", "H", "U"):
            text_value += 0.95
        elif c in ("w", "N", "O", "Q", "%"):
            text_value += 1.0
        elif c in ("m", "W"):
            text_value += 1.15
        elif c == "M":
            text_value += 1.2
        elif c == "@":
            text_value += 1.3

    return "═" * math.ceil(text_value)

################################################################################
def titleize(text: str) -> str:

    return re.sub(
        r"[A-Za-z]+('[A-Za-z]+)?",
        lambda word: word.group(0).capitalize(),
        text
    )

################################################################################
def fuzzy_match(t1: str, t2: str) -> float:

    return fuzz.ratio(t1, t2)

################################################################################
class _NotSet:

    def __eq__(self, other: Any) -> bool:

        return False

    def __bool__(self) -> bool:

        return False

    def __str__(self) -> str:

        return "`Not Set`"

NS = _NotSet()

################################################################################
TimestampStyle = Literal["f", "F", "d", "D", "t", "T", "R"]
################################################################################
def format_timestamp(dt: datetime, style: TimestampStyle | None = None) -> str:
    """A helper function to format a :class:`datetime.datetime` for presentation within Discord.

    This allows for a locale-independent way of presenting data using Discord specific Markdown.

    +-------------+----------------------------+-----------------+
    |    Style    |       Example Output       |   Description   |
    +=============+============================+=================+
    | t           | 22:57                      | Short Time      |
    +-------------+----------------------------+-----------------+
    | T           | 22:57:58                   | Long Time       |
    +-------------+----------------------------+-----------------+
    | d           | 17/05/2016                 | Short Date      |
    +-------------+----------------------------+-----------------+
    | D           | 17 May 2016                | Long Date       |
    +-------------+----------------------------+-----------------+
    | f (default) | 17 May 2016 22:57          | Short Date Time |
    +-------------+----------------------------+-----------------+
    | F           | Tuesday, 17 May 2016 22:57 | Long Date Time  |
    +-------------+----------------------------+-----------------+
    | R           | 5 years ago                | Relative Time   |
    +-------------+----------------------------+-----------------+

    Note that the exact output depends on the user's locale setting in the client. The example output
    presented is using the ``en-GB`` locale.

    .. versionadded:: 2.0

    Parameters
    ----------
    dt: :class:`datetime.datetime`
        The datetime to format.
    style: :class:`str`
        The style to format the datetime with.

    Returns
    -------
    :class:`str`
        The formatted string.
    """
    if style is None:
        return f"<t:{int(dt.timestamp())}>"

    return f"<t:{int(dt.timestamp())}:{style}>"

################################################################################
async def edit_message_helper(interaction: Interaction, *args, **kwargs) -> None:

    try:
        await interaction.message.edit(*args, **kwargs)
    except:
        try:
            await interaction.edit_original_response(*args, **kwargs)
        except:
            print("Edit Message Helper FAILED")

################################################################################
