from databases import Database
from ..config.config import DATABASE_URL
from sqlalchemy import create_engine, MetaData

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
