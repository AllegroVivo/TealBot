from __future__ import annotations

from discord import Embed, EmbedField, Interaction
from typing import TYPE_CHECKING, Dict, Optional, Tuple, Type, TypeVar

from utilities import *

if TYPE_CHECKING:
    pass
################################################################################

__all__ = (
    "TCommissionType",
)

CI = TypeVar("CI", bound="TCommissionItem")

################################################################################
class TCommissionType:

    __slots__ = (
        "_id",
        "_name",
        "_price",
        "_description",
    )

################################################################################
    def __init__(
        self,
        _id: str,
        name: str,
        price: int,
        description: str,
    ):

        self._id: str = _id
        self._name: str = name
        self._price: int = price
        self._description: Optional[str] = description

################################################################################
    @classmethod
    def new(cls: Type[CI], name: str, price: int, description: Optional[str]) -> CI:

        type_id = new_commission_type(name, price, description)

        return cls(
            _id=type_id,
            name=name,
            price=price,
            description=description,
        )

################################################################################
    @classmethod
    def load(cls, data: Tuple[str, str, int, str]) -> CI:

        return cls(
            _id=data[0],
            name=data[1],
            price=data[2],
            description=data[3],
        )

################################################################################
    def __eq__(self, other: TCommissionType) -> bool:

        return self.id == other.id

################################################################################
    @property
    def id(self) -> str:

        return self._id

################################################################################
    @property
    def name(self) -> str:

        return self._name

################################################################################
    @name.setter
    def name(self, value: str) -> None:

        self._name = value
        self.update()

################################################################################
    @property
    def price(self) -> int:

        return self._price

################################################################################
    @price.setter
    def price(self, value: int) -> None:

        self._price = value
        self.update()

################################################################################
    @property
    def description(self) -> str:

        return self._description

################################################################################
    @description.setter
    def description(self, value: str) -> None:

        self._description = value
        self.update()

################################################################################
    def status(self) -> Embed:

        pass

################################################################################
    def update(self) -> None:

        c = db_connection.cursor()
        c.execute(
            "UPDATE commission_types SET name = %s, description = %s, price = %s "
            "WHERE type_id = %s",
            (
                self.name, self.description, self.price, self.id
            )
        )

        db_connection.commit()
        c.close()

        return

################################################################################
