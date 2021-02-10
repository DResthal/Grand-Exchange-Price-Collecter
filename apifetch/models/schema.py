from sqlalchemy import create_engine, Date, Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
Base = declarative_base()

class Items(Base):
    __tablename__ = "items"

    id = Column('item_id', Integer, primary_key=True)
    name = Column('name', String, unique=True, nullable=False)
    item_type = Column('item_type', String, nullable=False)
    icon = Column('icon', String, unique=True, nullable=False)
    description = Column('description', Text, nullable=False)
    is_members = Column('is_members', Boolean, nullable=False)

class Prices(Base):
    __tablename__ = "prices"

    id = Column('item_id', Integer, primary_key=True)
    date = Column('date', Date, primary_key=True)
    price = Column('price', Integer, nullable=False)
    trend = Column('trend', String, nullable=False)
    change_today = Column('change_today', Integer, nullable=False)

engine = create_engine(f"postgresql://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@localhost:5432/grandexchange")
Base.metadata.create_all(bind=engine)