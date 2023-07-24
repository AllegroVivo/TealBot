from __future__ import annotations

from discord import Guild, NotFound, TextChannel
from typing import TYPE_CHECKING, Optional, Tuple

from utilities import *

if TYPE_CHECKING:
    from classes.bot import TealBot
################################################################################

__all__ = (
    "TConfiguration",
)

################################################################################
class TConfiguration:

    __slots__ = (
        "_parent",
        "_comm_post_channel",
    )

################################################################################
    def __init__(self, guild: Guild):

        self._parent: Guild = guild

        self._comm_post_channel: Optional[TextChannel] = None

################################################################################
    @property
    def guild(self) -> Guild:

        return self._parent

################################################################################
    @property
    def comm_post_channel(self) -> Optional[TextChannel]:

        return self._comm_post_channel

################################################################################
    async def load_channels(self, data: Tuple[int, ...]) -> None:

        self._comm_post_channel = self.guild.get_channel(data[0])
        if self._comm_post_channel is None:
            try:
                self._comm_post_channel = self.guild.fetch_channel(data[0])
            except NotFound:
                # We can just push an update while the post channel is still None,
                # effectively removing the post channel from the database.
                self.update()

################################################################################
    def update(self) -> None:

        channel_id = self.comm_post_channel.id if self.comm_post_channel else None

        c = db_connection.cursor()
        c.execute(
            "UPDATE config SET post_channel = %s WHERE guild_id = %s",
            (channel_id, self.guild.id)
        )

        db_connection.commit()
        c.close()

        return

################################################################################
