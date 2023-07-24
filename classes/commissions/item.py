from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar

from .comm_type import TCommissionType
from utilities import *

if TYPE_CHECKING:
    from .commission import TCommission
################################################################################

__all__ = (
    "TCommissionType",
)

CI = TypeVar("CI", bound="TCommissionItem")


################################################################################
class TCommissionItem:

    __slots__ = (
        "_id",
        "_commission",
        "_type",
        "_quantity",
        "_complete",
        "_notes",
    )

################################################################################
    def __init__(
        self,
        _id: int,
        commission: TCommission,
        _type: TCommissionType,
        quantity: int,
        notes: Optional[str],
    ):

        self._id: int = _id
        self._commission: TCommission = commission

        self._type: TCommissionType = _type
        self._quantity: int = quantity
        self._complete: bool = False

        self._notes: Optional[str] = notes

################################################################################
    @classmethod
    def new(
        cls: Type[CI],
        parent: TCommission,
        _type: TCommissionType,
        quantity: int
    ) -> CI:

        item_id = new_commission_item(parent.id, _type.id, quantity, False)

        return cls(
            _id=item_id,
            commission=parent,
            _type=_type,
            quantity=quantity,
            notes=None,
        )

################################################################################
    @property
    def id(self) -> int:

        return self._id

################################################################################
    @property
    def parent(self) -> TCommission:

        return self._commission

################################################################################
    @property
    def item_type(self) -> TCommissionType:

        return self._type

################################################################################
    @property
    def quantity(self) -> int:

        return self._quantity

################################################################################
    @property
    def notes(self) -> Optional[str]:

        return self._notes

################################################################################
    def __eq__(self, other: TCommissionType) -> bool:

        return self.id == other.id

################################################################################
    def update(self) -> None:

        c = db_connection.cursor()
        c.execute(
            "UPDATE commission_items SET quantity = %s, notes = %s, completed = %s "
            "WHERE item_id = %s",
            (
                self.quantity, self.notes, self._complete, self.id
            )
        )

        db_connection.commit()
        c.close()

        return

################################################################################
