
import sys

from preproc import *
from ner import *
from attractions import *
from descriptions import *

####################

def main():
	if len(sys.argv) != 3: print('USAGE: python3 train.py {TRAIN_DIR} {MODEL_DIR}')
	else:
		training = train_step(sys.argv[1], sys.argv[2])


def process_summaries(input_dir):
    """Create training data structure from summary.out files"""
    ret = {}
    for subdirname in os.listdir(input_dir): #{country}-annot{n}
        if os.path.isdir(os.path.join(dirname,subdirname)):
            ret[subdirname] = {}
            summary_file = os.path.join(input_dir,subdirname,'4-output', 'summary.out')
            if os.path.isfile(summary_file):
                print(summary_file)
                    #ret[subdirname][doc] = filename_to_doc(os.path.join(dirname,subdirname,'3-txt',filename))

def train_step(input_dir, model_dir):

	#####	STEP 1 : preproc.py			#####
	#docs = dirname_to_docs('../annot2/3-txt')
	#docs = dirname_to_docs(input_dir)

    process_summaries(input_dir)
    #####	STEP 2 : ner.py				#####
    entities = docs_to_named_entities(docs)

	#####	STEP 3 : attractions.py		#####
	attractions = docs_and_entities_to_attractions(docs,entities)

	#####	STEP 4 : descriptions.py	#####
	attractions = add_descriptions_to_attractions(docs,attractions)

####################

if __name__ == "__main__":
	main()

####################