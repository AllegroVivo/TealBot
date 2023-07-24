from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from discord import Interaction, User

from .client import TClient

if TYPE_CHECKING:
    from classes.bot import TealBot
################################################################################

__all__ = (
    "TClientManager"
)

################################################################################
class TClientManager:

    __slots__ = (
        "_parent",
        "_clients",
    )

################################################################################
    def __init__(self, parent: TealBot):

        self._parent: TealBot = parent
        self._clients: Dict[int, TClient] = {}  # Maps Discord user ID to Client object.

################################################################################
    def __getitem__(self, key: Union[int, User]) -> Optional[TClient]:

        if isinstance(key, User):
            key = key.id

        try:
            return self._clients[key]
        except KeyError:
            return None

################################################################################
    def __contains__(self, key: int) -> bool:

        return key in self._clients

################################################################################
    @property
    def clients(self) -> List[TClient]:

        return [c for c in self._clients.values()]

################################################################################
    async def add_client(self, interaction: Interaction, user: User) -> TClient:

        new_client = TClient.new(user)
        self._clients[user.id] = new_client

        return new_client

################################################################################
    def load_client(self, user: User, data: Tuple[Any, ...]):

        self._clients[user.id] = TClient.load(user, data)

################################################################################
