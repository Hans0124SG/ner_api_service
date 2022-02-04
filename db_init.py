from sqlalchemy import create_engine, MetaData, ForeignKey
from sqlalchemy import Table, Column, Date, Integer, String

engine = create_engine('sqlite:///./scraped_entities.db', echo=True)

metadata_obj = MetaData()

# table to store the urls of the scraped webpages
urls = Table('urls', metadata_obj,
    Column('url_id', Integer, primary_key=True),
    Column('url', String(2048), nullable=False)
)

# table to store the named entities of the scraped webpages
entities = Table('entities', metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('entity', String(100), nullable=False),
    Column('url_id', Integer, ForeignKey("urls.url_id"), nullable=False),
    Column('text', String(100), nullable=False))

metadata_obj.create_all(engine)