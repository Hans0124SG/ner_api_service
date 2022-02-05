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

def checkIfEntityExists(connection: sqlalchemy.engine.base.Connection, entities: sqlalchemy.sql.schema.Table, entity: str) -> bool:
	'''
	Check if the query entity already exists in the database

			Parameters:
					connection (sqlalchemy.engine.base.Connection): The active database connection
					entities (sqlalchemy.sql.schema.Table): The entities table in the database
					entity (string): The query entity

			Returns:
					length_of_result (bool): whether there is at least one record with same entity in the database 
	'''
	result = connection.execute(
		select([entities.c.id]).
    	where(entities.c.entity == entity)
		)
	return len(result.fetchall()) > 0

def insertSingleRecord(connection: sqlalchemy.engine.base.Connection, tables: sqlalchemy.util._collections.immutabledict, url: str, entities: List[Tuple[str, str]]) -> str:
	'''
	Insert the scraped entities into the database

			Parameters:
					connection (sqlalchemy.engine.base.Connection): The active database connection
					tables (sqlalchemy.util._collections.immutabledict): The tables in the database
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

def retrieveAllEntities(connection: sqlalchemy.engine.base.Connection, tables: sqlalchemy.util._collections.immutabledict) -> Tuple[str, List[str]]:
	'''
	Retrieve all entities in the database

			Parameters:
					connection (sqlalchemy.engine.base.Connection): The active database connection
					tables (sqlalchemy.util._collections.immutabledict): The tables in the database
			Returns:
					entities (list): unique entities in the database
	'''
	entities_table = tables['entities']
	results = list(set([ent[0] for ent in connection.execute(select([entities_table.c.entity])).fetchall()]))
	if len(results) == 0:
		return ('No entities was found in the database', [])
	else:
		return ('Successfully retrieved', results)

def searchEntity(connection: sqlalchemy.engine.base.Connection, tables: sqlalchemy.util._collections.immutabledict, entity: str) -> Tuple[str, List[str]]:
	'''
	Retrieve all entities in the database

			Parameters:
					connection (sqlalchemy.engine.base.Connection): The active database connection
					tables (sqlalchemy.util._collections.immutabledict): The tables in the database
			Returns:
					entities (list): unique entities in the database
	'''
	entities_table = tables['entities']
	try:
		if checkIfEntityExists(connection, entities_table, entity):
			results = list(set([ent[0] for ent in connection.execute(select([entities_table.c.text]).where(entities_table.c.entity == entity)).fetchall()]))
			return ('Successfully retrieved', results)
		else:
			return ('Entity was not found in the database', [])
	except:
		return ('Unknown error', [])

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

def test2():
	db_path = 'sqlite:///./scraped_entities.db'
	engine = create_engine(db_path)
	meta_data = MetaData(bind=engine)
	MetaData.reflect(meta_data)
	tables = meta_data.tables
	with engine.connect() as connection:
		result = retrieveAllEntities(connection, tables)
		print(result)

def test3():
	db_path = 'sqlite:///./scraped_entities.db'
	engine = create_engine(db_path)
	meta_data = MetaData(bind=engine)
	MetaData.reflect(meta_data)
	tables = meta_data.tables
	with engine.connect() as connection:
		result = searchEntity(connection, tables, 'LOC')
		print(result)

if __name__ == '__main__':
	test()
	test2()
	test3()



