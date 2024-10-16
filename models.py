from sqlalchemy import Table, Column, Integer, String, DateTime, ARRAY, ForeignKey
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

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("client_pk", Integer, ForeignKey("clients.id"), nullable=False),
    Column("specialist_pk", Integer, ForeignKey("specialists.id"), nullable=False),
    Column("specialization", String, nullable=False),
    Column("status", String, nullable=False),
    Column("comment", String, nullable=True),
    Column("timestamp", DateTime, default=func.now(), nullable=False),
)
