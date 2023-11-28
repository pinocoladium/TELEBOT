import os

import psycopg2
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")

PG_DSN = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
conn = psycopg2.connect(
    user=PG_USER, database=PG_DB, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT
)

engine = create_engine(PG_DSN)
Session = sessionmaker(engine)
Base = declarative_base()


class Wish_list(Base):
    __tablename__ = "wish_list_table"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(50), nullable=False)
    image_path = Column(String(50), nullable=False)
    description = Column(String, nullable=False)
    link = Column(String, nullable=False)
