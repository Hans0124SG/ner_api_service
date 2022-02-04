from typing import List, Tuple
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.sql import select

def checkIfURLExists(connection: sqlalchemy.engine.base.Connection, urls: sqlalchemy.sql.schema.Table, url: str) -> bool:
	'''
	Check if the query url already exists in the database

			Parameters:
					connection (sqlalchemy.engine.base.Connection): The active database connection
					urls (sqlalchemy.sql.schema.Table): The urls table in the database
					url (string): The query url

			Returns:
					length_of_result (bool): whether there is at least one record with same url in the database 
	'''
	result = connection.execute(
		select([urls.c.url_id]).
    	where(urls.c.url == url)
		)
	return len(result.fetchall()) > 0

def insertSingleRecord(connection: sqlalchemy.engine.base.Connection, tables: sqlalchemy.util._collections.immutabledict, url: str, entities: List[Tuple[str, str]]) -> str:
	'''
	Insert the scraped entities into the database

			Parameters:
					connection (sqlalchemy.engine.base.Connection): The active database connection
					tables (sqlalchemy.util._collections.immutabledict): The urls table in the database
					url (string): The query url

			Returns:
					length_of_result (bool): whether there is at least one record with same url in the database 
	'''
	urls_table = tables['urls']
	entities_table = tables['entities']

	try:
		if checkIfURLExists(connection, urls_table, url):
			return 'URL existed, entities are not populated'
		else:
			new_url_id = connection.execute(urls_table.insert().values(url=url)).lastrowid
			for text, ent in entities:
				connection.execute(entities_table.insert().values(entity=ent, text=text, url_id=new_url_id))
		return 'New entities successfully populated'
	except:
		return 'Unknown error'

def test():
	db_path = 'sqlite:///./scraped_entities.db'
	url = "www.google.com"
	engine = create_engine(db_path)
	meta_data = MetaData(bind=engine)
	MetaData.reflect(meta_data)
	tables = meta_data.tables
	entities = [('test_entity', 'test_text')]
	with engine.connect() as connection:
		print(checkIfURLExists(connection, tables['urls'], url))
		insertSingleRecord(connection, tables, url, entities)

if __name__ == '__main__':
	test()



