from enum   import Enum
################################################################################

__all__ = (
    "CommissionType",
    "ClientTag",
    "CommunicationMethod",
    "CommissionStatus",
    "CommissionTag",
)

################################################################################
class CommissionType(Enum):

    Chibi = 1
    Chibify = 2
    Emote = 3
    Sticker = 4
    TwitchPanel = 5
    TwitchSubBadge = 6
    TwitchSubFlair = 7
    TwitchScene = 8
    Avatar = 9
    Other = 10

################################################################################
class ClientTag(Enum):

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
class CommunicationMethod(Enum):

    Discord = 1
    Email = 2
    Other = 3

################################################################################
class CommissionStatus(Enum):

    Pending = 1
    InProgress = 2
    Completed = 3
    Cancelled = 4
    Refunded = 5
    Other = 6

################################################################################
class CommissionTag(Enum):

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
