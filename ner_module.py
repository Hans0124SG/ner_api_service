from typing import List, Tuple

class NERModule():
	'''
	Basic Class of our NER module. Future NER models should inherit this class.
	'''

	def __init__(self):
		'''
		Initialization of the NER model.
		'''
		pass

	def getListOfEntities(self, input: str) -> List[Tuple[str, str]]:
		'''
		Returns the list of entities and corresponding text extracted from the input.

				Parameters:
						input (string): The input text body

				Returns:
						list_of_entities (list): List of tuples (entity, text)
		'''
		return [(None,None)]

class spacyNER(NERModule):

	def __init__(self):
		import spacy
		super().__init__()
		self.model = spacy.load("en_core_web_sm")

	def getListOfEntities(self, input):
		results = []

		try:
			output = self.model(input)
		except (ValueError, AttributeError, TypeError):
			raise AssertionError('Input should be a string')
		
		for ent in output.ents:
			results.append((ent.text,ent.label_))

		return results

def test():
	raw_text = "The Indian Space Research Organisation or is the national space agency of India, headquartered in Bengaluru. It operates under Department of Space which is directly overseen by the Prime Minister of India while Chairman of ISRO acts as executive of DOS as well."
	NER_model = spacyNER()
	results = NER_model.getListOfEntities(raw_text)
	print(results)

if __name__ == '__main__':
	test()
