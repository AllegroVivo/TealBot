from __future__ import annotations

from datetime import datetime
from discord import Colour, Embed, User
from typing import TYPE_CHECKING, Optional

from assets import BotImages

if TYPE_CHECKING:
    pass
################################################################################

__all__ = (
    "TErrorMessage",
    "ClientAlreadyExistsError"
)

################################################################################
class TErrorMessage(Embed):
    """A subclassed Discord embed object acting as an error message."""

    def __init__(
        self,
        *,
        title: str,
        message: str,
        solution: str,
        description: Optional[str] = None
    ):

        super().__init__(
            title=title,
            description=description if description is not None else Embed.Empty,
            colour=Colour.red()
        )

        self.add_field(
            name="What Happened?",
            value=message,
            inline=True,
        )

        self.add_field(
            name="How to Fix?",
            value=solution,
            inline=True
        )

        self.timestamp = datetime.now()
        self.set_thumbnail(url=BotImages.ErrorFrog)

################################################################################
class ClientAlreadyExistsError(TErrorMessage):

    def __init__(self, user: User):
        super().__init__(
            title="Client Already Exists",
            message=f"A client already exists for user {user.mention}.",
            solution="Please use the `/clients status` command to edit information."
        )

################################################################################
