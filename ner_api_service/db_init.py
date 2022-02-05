from sqlalchemy import create_engine, MetaData, ForeignKey
from sqlalchemy import Table, Column, Date, Integer, String, Text
import os

engine = create_engine('sqlite:///../database/scraped_entities.db', echo=True)

metadata_obj = MetaData()

# table to store the urls of the scraped webpages
sources = Table('sources', metadata_obj,
    Column('source_id', Integer, primary_key=True),
    Column('source_type', String(100), nullable=False),
    Column('source', String(2048), nullable=False),
    Column('text', Text, nullable=False)
)

# table to store the named entities of the scraped webpages
entities = Table('entities', metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('entity', String(100), nullable=False),
    Column('source_id', Integer, ForeignKey("sources.source_id"), nullable=False),
    Column('text', String(100), nullable=False))

metadata_obj.create_all(engine)