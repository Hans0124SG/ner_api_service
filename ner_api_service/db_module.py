from typing import List, Tuple
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.sql import select
import pandas as pd

def checkIfSourceExists(connection: sqlalchemy.engine.base.Connection, sources: sqlalchemy.sql.schema.Table, source: str) -> bool:
	'''
	Check if the query source already exists in the database

			Parameters:
					connection (sqlalchemy.engine.base.Connection): The active database connection
					sources (sqlalchemy.sql.schema.Table): The sources table in the database
					source (string): The query source

			Returns:
					length_of_result (bool): whether there is at least one record with same source in the database 
	'''
	result = connection.execute(
		select([sources.c.source_id]).
    	where(sources.c.source == source)
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

def insertSingleRecord(connection: sqlalchemy.engine.base.Connection, tables: sqlalchemy.util._collections.immutabledict, source_type: str, source: str, raw_text: str, entities: List[Tuple[str, str]]) -> str:
	'''
	Insert the entities into the database

			Parameters:
					connection (sqlalchemy.engine.base.Connection): The active database connection
					tables (sqlalchemy.util._collections.immutabledict): The tables in the database
					source_type (string): The type of the source (e.g. webpage, database, csv_file)
					source (string): The query source
					raw_text (string): The query text
					entities (List[Tuple[str, str]]): The extracted entities

			Returns:
					message (string): The status message of the action 
	'''
	sources_table = tables['sources']
	entities_table = tables['entities']

	try:
		if checkIfSourceExists(connection, sources_table, source):
			return 'Source existed, entities are not populated'
		else:
			new_source_id = connection.execute(sources_table.insert().values(source_type=source_type, source=source, text=raw_text)).lastrowid
			for text, ent in entities:
				connection.execute(entities_table.insert().values(entity=ent, text=text, source_id=new_source_id))
		return 'New entities successfully populated'
	except:
		return 'Unknown error'

def insertDataFrameRecord(connection: sqlalchemy.engine.base.Connection, tables: sqlalchemy.util._collections.immutabledict, batch_sources: pd.DataFrame) -> str:
	'''
	Insert a pandas dataframe of entities into the database

			Parameters:
					connection (sqlalchemy.engine.base.Connection): The active database connection
					tables (sqlalchemy.util._collections.immutabledict): The tables in the database
					batch_sources (pd.DataFrame): A dataframe of extracted entities from multiple sources with columns [source_type, source, text, entities]

			Returns:
					message (string): The status message of the action 
	'''
	responses = set()
	for index, row in batch_sources.iterrows():
		response = insertSingleRecord(connection, tables, row['source_type'], row['source'], row['text'], row['entities'])
		responses.add(response)
	if 'Unknown error' in responses:
		return 'Unknown error'
	elif 'Source existed, entities are not populated' in responses:
		return 'At least some sources are existed in the database and not populated'
	else:
		return 'New entities are successfully populated for each entry'


def retrieveAllEntities(connection: sqlalchemy.engine.base.Connection, tables: sqlalchemy.util._collections.immutabledict) -> Tuple[str, List[str]]:
	'''
	Retrieve all entities in the database

			Parameters:
					connection (sqlalchemy.engine.base.Connection): The active database connection
					tables (sqlalchemy.util._collections.immutabledict): The tables in the database
			Returns:
					content (Tuple[str, List[str]]): Status message and the unique entities in the database
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
					content (Tuple[str, List[str]]): Status message and all corresponding text of the entity in the database
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
	source = "www.google.com"
	source_type = 'url'
	engine = create_engine(db_path)
	meta_data = MetaData(bind=engine)
	MetaData.reflect(meta_data)
	tables = meta_data.tables
	entities = [('test_text', 'test_entity')]
	with engine.connect() as connection:
		print(checkIfSourceExists(connection, tables['sources'], source))
		print(insertSingleRecord(connection, tables, 'webpage', source, entities))

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



