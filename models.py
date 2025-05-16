from typing import Optional
import os
from sqlalchemy import  String, create_engine
from sqlalchemy.orm import mapped_column, relationship, declarative_base, Mapped
from dotenv import load_dotenv
from databases import Database


load_dotenv()
SQLALCHEMY_URI = os.getenv("SQLALCHEMY_URI")
engine = create_engine(SQLALCHEMY_URI, echo=True)
database = Database(SQLALCHEMY_URI)
Base = declarative_base()



class House(Base):
    __tablename__ = "houses"

    index: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    house: Mapped[str] = mapped_column(String(50))
    animal: Mapped[str] = mapped_column(String(50))


Base.metadata.create_all(bind=engine)