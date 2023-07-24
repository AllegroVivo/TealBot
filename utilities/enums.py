from discord import SelectOption
from enum   import Enum
from typing import List
################################################################################

__all__ = (
    "ClientTag",
    "CommunicationMethod",
    "CommissionStatus",
    "CommissionTag",
)

################################################################################
class TealEnum(Enum):

    @property
    def proper_name(self) -> str:

        return self.name

################################################################################
class ClientTag(TealEnum):

    # General
    Active = 1
    Inactive = 2
    Blacklist = 3
    # Commission
    Commission = 4
    # Payment
    Paid = 5
    Unpaid = 6
    # Communication
    Discord = 7
    Email = 8
    # Special
    Friend = 9
    # Other
    Other = 10

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:

        return [
            SelectOption(label=option.proper_name, value=str(option.value))
            for option in ClientTag
        ]

################################################################################
class CommunicationMethod(TealEnum):

    Discord = 1
    Email = 2
    Other = 3

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:

        return [
            SelectOption(label=option.proper_name, value=str(option.value))
            for option in CommunicationMethod
        ]

################################################################################
class CommissionStatus(TealEnum):

    Pending = 1
    InProgress = 2
    Completed = 3
    Cancelled = 4
    Refunded = 5
    Other = 6

################################################################################
class CommissionTag(TealEnum):

    # General
    Commission = 1
    # Status
    Pending = 2
    InProgress = 3
    Completed = 4
    Cancelled = 5
    Refunded = 6
    # Payment
    Paid = 7
    Unpaid = 8
    # Type
    Chibi = 9
    Chibify = 10
    Emote = 11
    Sticker = 12
    TwitchPanel = 13
    TwitchSubBadge = 14
    TwitchSubFlair = 15
    TwitchScene = 16
    Avatar = 17
    Other = 18

################################################################################
