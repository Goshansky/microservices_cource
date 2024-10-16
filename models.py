from sqlalchemy import Table, Column, Integer, String, DateTime, ARRAY
from sqlalchemy.sql import func
from database import metadata

clients = Table(
    "clients",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("last_name", String, nullable=False),
    Column("first_name", String, nullable=False),
    Column("middle_name", String, nullable=True),
    Column("email", String, nullable=False, unique=True),
    Column("phone_number", String, nullable=False, unique=True),
    Column("password", String, nullable=False),
    Column("timestamp", DateTime, default=func.now(), nullable=False),
)

specialists = Table(
    "specialists",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("last_name", String, nullable=False),
    Column("first_name", String, nullable=False),
    Column("middle_name", String, nullable=True),
    Column("email", String, nullable=False, unique=True),
    Column("phone_number", String, nullable=False, unique=True),
    Column("password", String, nullable=False),
    Column("specialization", ARRAY(String), nullable=False),
    Column("timestamp", DateTime, default=func.now(), nullable=False),
)
