from __future__ import annotations

import os
import psycopg2
import uuid

from datetime import datetime
from discord import Guild, User
from dotenv import load_dotenv
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from psycopg2.extensions import cursor
################################################################################

__all__ = (
    "db_connection",
    "assert_db_structure",
    "new_commission_entry",
    "new_client_entry",
    "new_commission_type",
    "new_commission_item",
    "assert_guild_records",
)

################################################################################

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

db_connection = psycopg2.connect(DATABASE_URL, sslmode="require")
print("Database connection initialized...")

################################################################################
def assert_db_structure() -> None:

    cur = db_connection.cursor()

    assert_system_tables(cur)
    assert_comm_tables(cur)

    db_connection.commit()
    cur.close()

    return

################################################################################
def assert_system_tables(c: cursor) -> None:

    c.execute(
        "CREATE TABLE IF NOT EXISTS config("
        "guild_id BIGINT UNIQUE NOT NULL,"
        "post_channel BIGINT,"
        "CONSTRAINT config_pkey PRIMARY KEY (guild_id))"
    )

    return

################################################################################
def assert_comm_tables(c: cursor) -> None:

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
        "commission_id TEXT UNIQUE NOT NULL,"
        "user_id BIGINT NOT NULL,"
        "CONSTRAINT commissions_pkey PRIMARY KEY (commission_id))"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS commission_details("
        "commission_id TEXT UNIQUE NOT NULL,"
        "tags TEXT,"
        "status INTEGER,"
        "notes TEXT,"
        "price INTEGER,"
        "vip BOOLEAN,"
        "rush BOOLEAN,"
        "paid BOOLEAN,"
        "CONSTRAINT commission_details_pkey PRIMARY KEY (commission_id))"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS commission_dates("
        "commission_id TEXT UNIQUE NOT NULL,"
        "create_date TIMESTAMP,"
        "update_date TIMESTAMP,"
        "start_date TIMESTAMP,"
        "deadline TIMESTAMP,"
        "paid_date TIMESTAMP,"
        "complete_date TIMESTAMP,"
        "CONSTRAINT commission_dates_pkey PRIMARY KEY (commission_id))"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS commission_items("
        "item_id TEXT UNIQUE NOT NULL,"
        "commission_id BIGINT NOT NULL,"
        "commission_type INTEGER,"
        "quantity INTEGER,"
        "completed BOOLEAN,"
        "CONSTRAINT commission_items_pkey PRIMARY KEY (item_id))"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS commission_types("
        "type_id SERIAL,"
        "name TEXT,"
        "description TEXT,"
        "price INTEGER,"
        "image TEXT,"
        "CONSTRAINT commission_types_pkey PRIMARY KEY (type_id))"
    )

    c.execute(
        "CREATE OR REPLACE VIEW commission_master AS "
        "SELECT c.commission_id,"
        "c.user_id,"
        "cd.tags,"
        "cd.status,"
        "cd.notes,"
        "cd.price,"
        "cd.vip,"
        "cd.rush,"
        "cd.paid,"
        "cdt.create_date,"
        "cdt.update_date,"
        "cdt.start_date,"
        "cdt.deadline,"
        "cdt.paid_date,"
        "cdt.complete_date "
        "FROM commissions c "
        "JOIN commission_details cd ON c.commission_id = cd.commission_id "
        "JOIN commission_dates cdt ON c.commission_id = cdt.commission_id;"
    )

    return

################################################################################
def new_commission_entry(
    user_id: int,
    price: int,
    vip: bool,
    rush: bool,
    create_date: Optional[datetime],
) -> str:

    commission_id = uuid.uuid4().hex

    c = db_connection.cursor()
    c.execute(
        "INSERT INTO commissions (commission_id, user_id) VALUES (%s, %s)",
        (commission_id, user_id)
    )
    c.execute(
        "INSERT INTO commission_details (commission_id, price, vip, rush) "
        "VALUES (%s, %s, %s, %s)",
        (commission_id, price, vip, rush)
    )
    c.execute(
        "INSERT INTO commission_dates (commission_id, create_date, update_date) "
        "VALUES (%s, %s, %s)",
        (commission_id, create_date, create_date)
    )

    db_connection.commit()
    c.close()

    return commission_id

################################################################################
def new_client_entry(user: User) -> None:

    c = db_connection.cursor()
    c.execute(
        "INSERT INTO clients (user_id, update_date) VALUES (%s, %s)",
        (user.id, datetime.now())
    )

    db_connection.commit()
    c.close()

    return

################################################################################
def new_commission_type(name: str, price: int, description: Optional[str]) -> int:

    c = db_connection.cursor()
    c.execute(
        "INSERT INTO commission_types (name, description, price) "
        "VALUES (%s, %s, %s) RETURNING type_id",
        (name, description, price)
    )

    type_id = c.fetchone()[0]

    db_connection.commit()
    c.close()

    return type_id

################################################################################
def new_commission_item(
    commission_id: str,
    commission_type: str,
    quantity: int,
    completed: bool
) -> str:

    item_id = uuid.uuid4().hex

    c = db_connection.cursor()
    c.execute(
        "INSERT INTO commission_items (item_id, commission_id, commission_type, "
        "quantity, completed) VALUES (%s, %s, %s, %s, %s)",
        (
            item_id, commission_id, commission_type, quantity, completed
        )
    )

    db_connection.commit()
    c.close()

    return item_id

################################################################################
def new_guild_entry(guild: Guild) -> None:

    c = db_connection.cursor()
    c.execute(
        "INSERT INTO config (guild_id) VALUES (%s)",
        (guild.id,)
    )

    db_connection.commit()
    c.close()

    return

################################################################################
def assert_guild_records(guilds: List[Guild]) -> None:

    c = db_connection.cursor()

    for guild in guilds:
        c.execute(
            "INSERT INTO config (guild_id) VALUES (%s) ON CONFLICT DO NOTHING",
            (guild.id,)
        )

    db_connection.commit()
    c.close()

    return

################################################################################
