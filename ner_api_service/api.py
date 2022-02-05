import os
from flask import Flask, request, jsonify
from flasgger import Swagger
from sqlalchemy import create_engine, MetaData
from ner_module import spacyNER
import scraping_module 
import db_module

app = Flask(__name__)
swagger = Swagger(app)
db_path = 'sqlite:///./scraped_entities.db'


@app.route("/recognize_entities", methods=['GET'])
def recognize_entities():
	"""Endpoint returning the named entities extracted from the text
	---
	parameters: 
    	- name: text
    	  in: query
    	  type: string
    	  required: true
	responses: 
		200: 
	  		description: text
	"""
	model = spacyNER()
	input = request.args.get('text')
	entities = model.getListOfEntities(input)
	if len(entities) == 0:
		status = 'No entities was recognized in the text'
	else:
		status = 'Successfully recognized'
	return jsonify(status=status, entities=entities)

@app.route("/scrape_url", methods=['POST'])
def scrape_url():
	"""Endpoint retrieving the named entities the body text in the url and persist the result into the database 
	---
	parameters: 
    	- name: url
    	  in: query
    	  type: string
    	  required: true
	responses: 
		200: 
	  		description: text
	"""
	url = request.args.get('url')
	input = scraping_module.scrapeSingleURL(url)
	model = spacyNER()
	entities = model.getListOfEntities(input)
	engine = create_engine(db_path)
	meta_data = MetaData(bind=engine)
	MetaData.reflect(meta_data)
	tables = meta_data.tables
	with engine.connect() as connection:
		response = db_module.insertSingleRecord(connection, tables, url, entities)

	return jsonify(status=response)

@app.route("/retrieve_entities", methods=['GET'])
def retrieve_entities():
	"""Endpoint retrieving the named entities in the database 
	---
	responses: 
		200: 
	  		description: text
	"""
	engine = create_engine(db_path)
	meta_data = MetaData(bind=engine)
	MetaData.reflect(meta_data)
	tables = meta_data.tables
	with engine.connect() as connection:
		results = db_module.retrieveAllEntities(connection, tables)

	return jsonify(status=results[0], entities=results[1])

@app.route("/search_entity", methods=['GET'])
def search_entity():
	"""Endpoint searching the corresponding text in the database given an entity
	---
	parameters: 
    	- name: entity
    	  in: query
    	  type: string
    	  required: true
	responses: 
		200: 
	  		description: text
	"""
	entity = request.args.get('entity')
	engine = create_engine(db_path)
	meta_data = MetaData(bind=engine)
	MetaData.reflect(meta_data)
	tables = meta_data.tables
	with engine.connect() as connection:
		results = db_module.searchEntity(connection, tables, entity)

	return jsonify(status=results[0], entities=results[1])

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
