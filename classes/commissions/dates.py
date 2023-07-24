from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional, Type, TypeVar

from utilities import *

if TYPE_CHECKING:
    from .commission import TCommission
################################################################################

__all__ = (
    "TCommissionDates",
)

CD = TypeVar("CD", bound="TCommissionDates")

################################################################################
class TCommissionDates:

    __slots__ = (
        "_parent",
        "_create",
        "_start",
        "_deadline",
        "_update",
        "_complete",
        "_paid"
    )

################################################################################
    def __init__(self, parent: TCommission, create_dt: datetime):

        self._parent: TCommission = parent

        self._create: datetime = create_dt
        self._update: datetime = create_dt

        self._start: Optional[datetime] = None
        self._deadline: Optional[datetime] = None
        self._complete: Optional[datetime] = None
        self._paid: Optional[datetime] = None

################################################################################
    @property
    def parent(self) -> TCommission:

        return self._parent

################################################################################
    @property
    def create_date(self) -> datetime:

        return self._create

################################################################################
    @property
    def start_date(self) -> Optional[datetime]:

        return self._start

################################################################################
    @start_date.setter
    def start_date(self, value: Optional[datetime]) -> None:

        self._start = value
        self.update()

################################################################################
    @property
    def deadline(self) -> Optional[datetime]:

        return self._deadline

################################################################################
    @deadline.setter
    def deadline(self, value: Optional[datetime]) -> None:

        self._deadline = value
        self.update()

################################################################################
    @property
    def update_date(self) -> datetime:

        return self._update

################################################################################
    @update_date.setter
    def update_date(self, value: datetime) -> None:

        self._update = value
        self.update()

################################################################################
    @property
    def complete_date(self) -> Optional[datetime]:

        return self._complete

################################################################################
    @complete_date.setter
    def complete_date(self, value: Optional[datetime]) -> None:

        self._complete = value
        self.update()

################################################################################
    @property
    def paid_date(self) -> Optional[datetime]:

        return self._paid

################################################################################
    @paid_date.setter
    def paid_date(self, value: Optional[datetime]) -> None:

        self._paid = value
        self.update()

################################################################################
    def update(self) -> None:

        c = db_connection.cursor()
        c.execute(
            "UPDATE commission_dates SET "
            "start_date = %s, deadline = %s, paid_date = %s, update_date = %s, "
            "complete_date = %s WHERE commission_id = %s",
            (
                self.start_date, self.deadline, self.paid_date, self.update_date,
                self.complete_date, self.parent.id
            )
        )

        db_connection.commit()
        c.close()

        return

################################################################################
