import os
from flask import Flask, request, jsonify, redirect, url_for
from flasgger import Swagger
from sqlalchemy import create_engine, MetaData
from ner_module import spacyNER
import preprocessing_module 
import db_module

app = Flask(__name__)

template = {
  "swagger": "2.0",
  "info": {
	"title": "NER API",
	"description": "A Named Entity Recognition API, able to recognize entities in text from websites, csv files and databases.",
	"version": "0.0.1"
  }
}

swagger = Swagger(app, template=template)
db_path = 'sqlite:////var/www/ner_api/database/scraped_entities.db'
model = spacyNER()

@app.route('/')
def hello():
	'''
	To redirect the homepage to the flasgger apidocs page
	'''
	return redirect(url_for('flasgger.apidocs'))

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
	input = request.args.get('text')
	entities = model.getListOfEntities(input)
	if len(entities) == 0:
		code = 204
		status = 'No entities was recognized in the text'
	else:
		code = 200
		status = 'Successfully recognized'
	return jsonify(code=code, status=status, entities=entities)

@app.route("/retrieve_from_url", methods=['POST'])
def retrieve_from_url():
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
	source = request.args.get('url')
	input = preprocessing_module.scrapeSingleURL(source)
	entities = model.getListOfEntities(input)

	# write to database
	engine = create_engine(db_path)
	meta_data = MetaData(bind=engine)
	MetaData.reflect(meta_data)
	tables = meta_data.tables
	with engine.connect() as connection:
		code, response = db_module.insertSingleRecord(connection, tables, 'webpage', source, input, entities)

	return jsonify(code=code, status=response)

@app.route("/retrieve_from_csv", methods=['POST'])
def retrieve_from_csv():
	"""Endpoint retrieving the named entities the body text in a csv and persist the result into the database 
	---
	parameters: 
		- name: csv_file
		  in: formData
		  type: file
		  required: true
		- name: text_col
		  in: query
		  type: string
		  required: true
		- name: source_col
		  in: query
		  type: string
		  required: true
		- name: source_type_col
		  in: query
		  type: string
		  required: true
	responses: 
		200: 
			description: text
	"""
	import pandas as pd
	text_col = request.args.get('text_col')
	source_col = request.args.get('source_col')
	source_type_col = request.args.get('source_type_col')
	csv_file = request.files.get('csv_file')
	batch_sources = pd.read_csv(csv_file).rename(columns={text_col: "text", source_type_col: "source_type", source_col: "source"})

	batch_sources['entities'] = batch_sources.text.apply(lambda x: model.getListOfEntities(x))

	engine = create_engine(db_path)
	meta_data = MetaData(bind=engine)
	MetaData.reflect(meta_data)
	tables = meta_data.tables
	with engine.connect() as connection:
		code, response = db_module.insertDataFrameRecord(connection, tables, batch_sources[['source_type', 'source', 'text', 'entities']])

	return jsonify(code=code, status=response)


@app.route("/retrieve_from_db", methods=['POST'])
def retrieve_from_db():
	"""Endpoint retrieving the named entities the body text in a database and persist the result into the database 
	---
	parameters: 
		- name: database_path
		  in: query
		  type: string
		  required: true
		- name: target_table
		  in: query
		  type: string
		  required: true
		- name: text_col
		  in: query
		  type: string
		  required: true
		- name: source_col
		  in: query
		  type: string
		  required: true
		- name: source_type_col
		  in: query
		  type: string
		  required: true
	responses: 
		200: 
			description: text
	"""
	import pandas as pd
	text_col = request.args.get('text_col')
	source_col = request.args.get('source_col')
	source_type_col = request.args.get('source_type_col')
	database_path = request.args.get('database_path')
	target_table = request.args.get('target_table')

	batch_sources = pd.read_sql_table(target_table, database_path).rename(columns={text_col: "text", source_type_col: "source_type", source_col: "source"})
	batch_sources['entities'] = batch_sources.text.apply(lambda x: model.getListOfEntities(x))

	engine = create_engine(db_path)
	meta_data = MetaData(bind=engine)
	MetaData.reflect(meta_data)
	tables = meta_data.tables
	with engine.connect() as connection:
		code, response = db_module.insertDataFrameRecord(connection, tables, batch_sources[['source_type', 'source', 'text', 'entities']])

	return jsonify(code=code, status=response)

@app.route("/show_entities", methods=['GET'])
def show_entities():
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

	return jsonify(code=results[0], status=results[1], entities=results[2])

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

	return jsonify(code=results[0], status=results[1], text=results[2])

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
