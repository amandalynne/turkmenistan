
import sys
from contextlib import contextmanager

####################

@contextmanager
def writeopen(outputfilename=None):
	if len(outputfilename) > 0: outputfile = open(outputfilename, 'w', encoding='utf-8')
	else: outputfile = sys.stdout
	try: yield outputfile
	finally:
		if outputfile is not sys.stdout: outputfile.close()

def print_attractions_to_filename(attractions, filename):
	try:
		with writeopen(filename) as outputfile:
			print('{', file=outputfile)
			for attraction in attractions:
				print(('\t'*1)+'"'+attraction+'" :', file=outputfile)
				print(('\t'*2)+'{', file=outputfile)
				print(('\t'*3)+'"category" : "'+attractions[attraction]['category']+'",', file=outputfile)

				print(('\t'*3)+'"instances" :', file=outputfile)
				print(('\t'*4)+'[', file=outputfile)
				for instance in attractions[attraction]['instances']:
					print(('\t'*5)+'{', file=outputfile)
					print(('\t'*6), '"indices" :', instance['indices'], ',', file=outputfile)
					print(('\t'*6), '"string" : "'+instance['string']+'",', file=outputfile)
					print(('\t'*6), '"category" : "'+instance['category']+'",', file=outputfile)
					print(('\t'*6), '"rank" :', instance['rank'], ',', file=outputfile)
					print(('\t'*5)+'}', file=outputfile)
				print(('\t'*4)+'],', file=outputfile)

				print(('\t'*3)+'"descriptions" :', file=outputfile)
				print(('\t'*4)+'[', file=outputfile)
				for instance in attractions[attraction]['descriptions']:
					print(('\t'*5)+'{', file=outputfile)
					print(('\t'*6), '"indices" :', instance['indices'], ',', file=outputfile)
					print(('\t'*6), '"string" : "'+instance['string']+'"', file=outputfile)
					print(('\t'*5)+'}', file=outputfile)
				print(('\t'*4)+'],', file=outputfile)

				print(('\t'*2)+'}', file=outputfile)
			print('}', file=outputfile)
	except Exception as err:
		print(err)

####################

