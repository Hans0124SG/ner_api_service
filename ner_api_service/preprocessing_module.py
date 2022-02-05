from bs4 import BeautifulSoup
import requests
import re

def scrapeSingleURL(url: str) -> str:
	'''
	Scrape and clean the body text of an url.

			Parameters:
					url (str): The url of the webpage to scrape

			Returns:
					body (str): The cleaned body text of the webpage
	'''
	html_content = requests.get(url).content
	soup = BeautifulSoup(html_content, "html.parser")
	body = soup.body.text
	
	# remove blankspaces
	body = body.replace('\n', ' ')
	body = body.replace('\t', ' ')
	body = body.replace('\r', ' ')
	body = body.replace('\xa0', ' ')

	return body

def test():

	url = "https://www.gic.com.sg/newsroom/all/gic-becomes-strategic-investor-in-intercontinental-energy-leading-green-fuels-company/"
	raw_text = scrapeSingleURL(url)
	from ner_module import spacyNER
	NER_model = spacyNER()
	results = NER_model.getListOfEntities(raw_text)
	print(results)

if __name__ == '__main__':
	test()


