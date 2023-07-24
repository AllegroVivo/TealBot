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
    "ClientAlreadyExistsError",
    "InvalidNumberError",
    "TypeNotFoundError",
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
class InvalidNumberError(TErrorMessage):

    def __init__(self, number: str):
        super().__init__(
            title="Invalid Number",
            description=f"Invalid value: |{number}|.",
            message=f"The value you entered at the prompt was not a valid number.",
            solution="Only enter whole numbers, nothing other than digits."
        )

################################################################################
class TypeNotFoundError(TErrorMessage):

    def __init__(self, invalid_id: int):
        super().__init__(
            title="Commission Type Not Found",
            message=f"No commission type exists with ID `{invalid_id}`.",
            solution=(
                "Check the footer of the embed for the commission type you want "
                "to edit for the correct ID."
            )
        )

################################################################################
