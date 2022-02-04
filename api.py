from flask import Flask, request, jsonify
from flasgger import Swagger
from sqlalchemy import create_engine, MetaData
from ner_module import spacyNER
import scraping_module 
import db_module

app = Flask(__name__)
swagger = Swagger(app)
db_path = 'sqlite:///./scraped_entities.db'


@app.route("/get_entities", methods=['GET'])
def get_entities():
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

	return jsonify(result=model.getListOfEntities(input))

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

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')