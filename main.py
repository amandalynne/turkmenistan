
import sys

from preproc import *
from ner import *
from attractions import *
from descriptions import *
from summary import *

####################

def main():
	if len(sys.argv) != 4: print('USAGE: python3 main.py {TRAIN_DIR} {TEST_DIR} {SUMMARY_FILE}')
	else:
		training = train_step(sys.argv[1])
		test_step(training, sys.argv[2], sys.argv[3])

####################

def train_step(dirname):
	return []

##########

# TODO: docs aren't separated by country... we probs want them to be?
def test_step(training,dirname,outputfile):

	#####	STEP 1 : preproc.py			#####
	#docs = dirname_to_docs('../annot2/3-txt')
	docs = dirname_to_docs(dirname)
	print_docs_to_filename(docs,'')

	#####	STEP 2 : ner.py				#####
	entities = docs_to_named_entities(docs)

	#####	STEP 3 : attractions.py		#####
	attractions = docs_and_entities_to_attractions(docs,entities)

	#####	STEP 4 : descriptions.py	#####
	attractions = add_descriptions_to_attractions(docs,attractions)

	#####	STEP 5 : summary.py			#####
	print_attractions_to_filename(attractions,'')
	#print_attractions_to_filename(attractions,argv[3])

####################

if __name__ == "__main__":
	main()

####################

