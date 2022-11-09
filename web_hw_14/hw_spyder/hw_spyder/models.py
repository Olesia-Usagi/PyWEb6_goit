from sqlalchemy import create_engine, Column, Table, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


assotiation_table = Table(
    "assotiation",
    Base.metadata,
    Column("keyword_id", ForeignKey("keyword.id")),
    Column("quote_id", ForeignKey("quote.id")),
)


class Quote(Base):
    __tablename__ = "quote"
    id = Column(Integer, primary_key=True)
    quote = Column('quote', Text(), nullable=False, unique=True)
    author_id = Column(Integer, ForeignKey("author.id"))
    # about = Column('about', Text())
    keywords = relationship(
        "Keyword", secondary=assotiation_table, back_populates="quotes"
    )


class Keyword(Base):
    __tablename__ = "keyword"
    id = Column(Integer, primary_key=True)
    key_word = Column('keywords', Text(), nullable=False, unique=True)
    quotes = relationship(
        "Quote", secondary=assotiation_table, back_populates="keywords"
    )


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    full_name = Column('full_name', Text(), nullable=False, unique=True)
    born_date = Column('born_date', Text())
    born_year = Column('born_year', Text())
    born_location = Column('born_location', Text())
    description = Column('description', Text())
    quote = relationship("Quote")

