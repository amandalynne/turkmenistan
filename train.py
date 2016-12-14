
import sys, re

from preproc import *
from ner import *
from attractions import *
from descriptions import *

####################

def main():
	if len(sys.argv) != 3: print('USAGE: python3 train.py {TRAIN_DIR} {MODEL_DIR}')
	else: training = train_step(sys.argv[1], sys.argv[2])

####################

def process_summaries(input_dir):
	"""Create training data structure from summary.out files"""
	ret = {}
	for subdirname in os.listdir(input_dir): #{country}-annot{n}
		if os.path.isdir(os.path.join(input_dir,subdirname)):
			ret[subdirname] = {}
			summary_file = os.path.join(input_dir,subdirname,'4-output', 'summary.out')
			if os.path.isfile(summary_file):
#				print(summary_file)
				with open(summary_file, encoding='latin-1') as inf:
					for line in inf.readlines():
#						print(line)
						pattern = r'^\s*\%+\s*(\w+\d+)\s+(\d+)/(\d+)\s+([^#]+)\s+##([^%]+)\s+%%(.*)$'
						match = re.match(pattern, line)
						if match:
							document = match.group(1).rstrip()
							attraction = match.group(4).rstrip()
							category = match.group(5).rstrip()
							description = match.group(6).rstrip()
							# need to take off leading whitespace
							ret[subdirname][attraction] = {}
							ret[subdirname][attraction]['desc'] = {}
							ret[subdirname][attraction]['desc'][document] =\
								(description, category)
#	print(ret['argentina-annot1'])
	return ret


def train_step(input_dir, model_dir):

	#####	STEP 1 : preproc.py			#####
	docs = dirname_to_docs(input_dir)
	#print_docs_to_filename(docs,'')

	#####	STEP 2 : process_summaries	#####
	entities = process_summaries(input_dir)

	#####	STEP 3 : attractions.py		#####
	attractions = docs_and_entities_to_attractions(docs,entities,model_dir, True)

	#attractions = add_descriptions_to_attractions(docs,attractions)
	#attractions = add_descriptions_to_attractions(docs,entities)
	attractions = generate_description_model(docs,entities)

####################

if __name__ == "__main__":
	main()

####################
