
import sys, os, shutil
from contextlib import contextmanager

from preproc import *
from ner import *
from attractions import *
from descriptions import *
from summary import *

####################

def main():
	if len(sys.argv) != 4: print('USAGE: python3 test.py {TEST_DIR} {MODEL_DIR} {OUTPUT_DIR}')
	else: test_step(sys.argv[1], sys.argv[2], sys.argv[3])

####################

@contextmanager
def writeopen(outputfilename=None):
	#if len(outputfilename) > 0: outputfile = open(outputfilename, 'w', encoding='utf-8')
	if len(outputfilename) > 0: outputfile = open(outputfilename, 'a', encoding='latin-1')
	else: outputfile = sys.stdout
	try: yield outputfile
	finally:
		if outputfile is not sys.stdout: outputfile.close()

def print_to_dot_out(attractions,output_dir):
	if output_dir[-1] is '/': output_dir = output_dir[:-1]
	for annot in attractions:
		if os.path.isdir(output_dir+'/'+annot):
			shutil.rmtree(output_dir+'/'+annot)
		if not os.path.isdir(output_dir+'/'+annot):
			os.mkdir(output_dir+'/'+annot)
		if not os.path.isdir(output_dir+'/'+annot+'/4-output'):
			os.mkdir(output_dir+'/'+annot+'/4-output')
		for attraction in attractions[annot]:
			for doc in attractions[annot][attraction]:
				filename = output_dir+'/'+annot+'/4-output/'+doc+'.out'
				#omit stuff that's descriptionless lol
				if len(attractions[annot][attraction][doc]['desc']):
					try:
						with writeopen(filename) as outputfile:
							print(attractions[annot][attraction][doc]['rank'].split('/')[0], attraction, '##'+attractions[annot][attraction][doc]['category'], '%% '+'; '.join(attractions[annot][attraction][doc]['desc']), file=outputfile, sep='\t')
					except Exception as err:
						print(err)

#####

# TODO: docs aren't separated by country... we probs want them to be?
def test_step(test_dir,model_dir,output_dir):

	#####	STEP 1 : preproc.py			#####
	docs = dirname_to_docs(test_dir)
	#print_docs_to_filename(docs,'')

	#####	STEP 2 : ner.py				#####
	attractions = docs_to_named_entities(docs)

	#####	STEP 4 : descriptions.py	#####
	attractions = add_descriptions_to_attractions(docs,attractions,model_dir)
	#print(attractions['turkmenistan-annot2'])

	#####	STEP 3 : attractions.py		#####
	#attractions = docs_and_entities_to_attractions(docs,entities)

	#####	STEP 5 : summary.py			#####
	#print_attractions_to_filename(attractions,'')
	#print_attractions_to_filename(attractions,argv[3])
	print_to_dot_out(attractions,output_dir)

####################

if __name__ == "__main__":
	main()

####################

