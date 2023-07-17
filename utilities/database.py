from __future__ import annotations

import os
import psycopg2

from dotenv import load_dotenv
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass
################################################################################

__all__ = (
    "db_connection",
)

################################################################################

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

db_connection = psycopg2.connect(DATABASE_URL, sslmode="require")
print("Database connection initialized...")

################################################################################
