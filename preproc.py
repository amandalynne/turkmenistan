
#import operator, numpy, math
import operator, math
import urllib.request, os, sys, re
from operator import itemgetter
from contextlib import contextmanager

####################

def float_str(num):
	ret = str(num)
	if (re.search(r'^\d*\.\d*?999+\d$',ret)):
		m = re.search(r'^(?P<LEFT>\d*)\.(?P<RIGHT>\d*?)999+\d$', ret)
		return '.'.join([m.group('LEFT') if m.group('LEFT') and m.group('RIGHT') else str(int(m.group('LEFT'))+1) if m.group('LEFT') else '1', str(int(m.group('RIGHT'))+1) if m.group('RIGHT') else '0'])
	elif (re.search(r'^\d*\.\d*?000+\d$',ret)):
		m = re.search(r'^(?P<LEFT>\d*)\.(?P<RIGHT>\d*?)000+\d$', ret)
		return '.'.join([m.group('LEFT') if m.group('LEFT') else '1', m.group('RIGHT') if m.group('RIGHT') else '0'])
	else: return ret

####################

def dirname_to_docs(dirname):
	ret = {}
	for subdirname in os.listdir(dirname): #{country}-annot{n}
		if os.path.isdir(os.path.join(dirname,subdirname)):
			country = subdirname.split('-')[0]
			for filename in os.listdir(os.path.join(dirname,subdirname,'3-txt')):
				if os.path.isfile(os.path.join(dirname,subdirname,'3-txt',filename)):
					doc = filename.split('.')[0]
					#ret[subdirname+'_'+filename.split('.')[0]] = filename_to_doc(os.path.join(dirname,subdirname,'3-txt',filename))
					ret['_'.join([country,doc])] = filename_to_doc(os.path.join(dirname,subdirname,'3-txt',filename))

#	for filename in os.listdir(dirname):
#		if os.path.isfile(os.path.join(dirname,filename)):
#			ret[filename.split('.')[0]] = filename_to_doc(os.path.join(dirname,filename))

	return ret

def filename_to_doc(filename):
	try:
		with open(filename, 'r', encoding='utf-8') as f:
			return list(filter(None,[line_to_sentences(line.strip()) for line in f.readlines()]))
	except Exception as err:
		print(err)

def line_to_sentences(line):
	#sentences = list(filter(None, [sent.strip().split() for sent in re.split('(\.|\!|\?)',line)]))
	return list(filter(None, [sent.strip().split() for sent in re.split('\.|\!|\?',line)]))

####################

@contextmanager
def writeopen(outputfilename=None):
	if len(outputfilename) > 0: outputfile = open(outputfilename, 'w', encoding='utf-8')
	else: outputfile = sys.stdout
	try: yield outputfile
	finally:
		if outputfile is not sys.stdout: outputfile.close()

def print_docs_to_filename(docs, filename):
	try:
		with writeopen(filename) as outputfile:
			print('{', file=outputfile)
			for doc in docs:
				print(('\t'*1)+'"'+doc+'" :', file=outputfile)
				print(('\t'*2)+'[', file=outputfile)
				for line in docs[doc]:
					print(('\t'*3)+'[', file=outputfile)
					for sent in line:
						print(('\t'*4), sent, file=outputfile)
					print(('\t'*3)+']', file=outputfile)
				print(('\t'*2)+']', file=outputfile)
			print('}', file=outputfile)
	except Exception as err:
		print(err)

####################

