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
    "assert_db_structure",
)

################################################################################

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

db_connection = psycopg2.connect(DATABASE_URL, sslmode="require")
print("Database connection initialized...")

################################################################################
def assert_db_structure() -> None:

    c = db_connection.cursor()

    c.execute(
        "CREATE TABLE IF NOT EXISTS clients("
        "user_id BIGINT UNIQUE NOT NULL,"
        "name TEXT,"
        "notes TEXT,"
        "tags TEXT,"
        "update_date TIMESTAMP,"
        "communication_method INTEGER,"
        "email TEXT,"
        "paypal TEXT,"
        "CONSTRAINT clients_pkey PRIMARY KEY (user_id))"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS commissions("
        "commission_id BIGINT UNIQUE NOT NULL,"
        "user_id BIGINT NOT NULL,"
        "items TEXT,"
        "tags TEXT,"
        "price INTEGER,"
        "description TEXT,"
        "notes TEXT,"
        "start_date TIMESTAMP,"
        "deadline TIMESTAMP,"
        "status INTEGER,"
        "paid BOOLEAN,"
        "paid_date TIMESTAMP,"
        "update_date TIMESTAMP,"
        "complete_date TIMESTAMP,"
        "CONSTRAINT commissions_pkey PRIMARY KEY (commission_id))"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS commission_items("
        "commission_id BIGINT NOT NULL,"
        "commission_type INTEGER,"
        "quantity INTEGER,"
        "completed BOOLEAN)"
    )

    db_connection.commit()
    c.close()

    return

################################################################################
def new_commission_entry(commission_id: int, user_id: int) -> None:

    c = db_connection.cursor()
    c.execute(
        "INSERT INTO commissions (commission_id, user_id) "
        "VALUES (%s, %s)",
        (commission_id, user_id)
    )

    db_connection.commit()
    c.close()

    return

################################################################################
def new_client_entry(user_id: int) -> None:

    c = db_connection.cursor()
    c.execute(
        "INSERT INTO clients (user_id) "
        "VALUES (%s)",
        (user_id,)
    )

    db_connection.commit()
    c.close()

    return

################################################################################
