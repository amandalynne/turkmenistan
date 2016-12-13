
#import operator, numpy, math
import operator, math
import urllib.request, os, sys, re
from operator import itemgetter
from contextlib import contextmanager

import nltk
#from nltk.corpus import wordnet as wn

####################

grammar = r"""
	NP:
		{<NN.*>+}
	JP:
		{<RB.*>*<JJ.*>}
	JP:
		{(<JP><,>)*<JP><,>?<CC><JP>}
	NP:
		{<DT|PRP\$|CD|JP|VB[N]>+<NP><PP>*}
	NP:
		{(<NP><,>)*<NP><,>?<CC><NP>}
	NP:
		{<RB.*>*<VB[GN]><RB.*>*<NP>}
	PP:
		{<IN|TO|RP><NP>}
	PP:
		{<RB.*>*<IN><RB|EX>}
	VP:
		{<MD>?<RB.*>*<VB[DPZ]?>+<RB.*>*<VB.*>*<EX>?<RB.*>*<IN|TO|RP>?}
	VP:
		{(<VP><,>)*<VP><,>?<CC><VP>}
	NP:
		{<RB.*>*<TO><RB.*>*<VB.*><RB.*>*<VB[GN]>*<RB.*>*}
	NP:
		{<RB.*>*<VB[GN]><RB.*>*}
	NP:
		{<NP><PP>}
	RV:
		{<WP|WDT|IN><VP>}
	NX:
		{<PRP|DT>}
	REL:
		{<RV><NP|NX>}
	NP:
		{<NP|NX><REL>}
	PRED:
		{<VP><PP>*<NP|NX|JP>*<PP>*}
	PROP:
		{<NP|NX><PRED>}
	REL:
		{<WP|WDT|WRB|IN><PROP>}
	NP:
		{<NP|NX><REL>}
	QUES:
		{<W.*><MD|VP>*<PRED|PROP><\.>*}
	IMP:
		{^<PRED>$}
	VOC:
		{<,>?<NP><,>?}
	PHR:
		{<CC>*<PROP|IMP|QUES|VOC>}
	PHR:
		{(<PHR><,>)*<PHR><,>?<CC><PHR>}
	SENT:
		{^<PHR><.>*}
"""

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

def remove_html(s):
	s = s.replace('\n','\\n')
	s = re.sub(r'<script>.*?</script>','',s)
	s = re.sub(r'<!--.*?-->','',s)
	s = re.sub(r'&nbsp;', ' ', s)
	s = re.sub(r'&[lr]squo;', '\'', s)
	s = re.sub(r'</?(h\d|p)>','\\n',s)
	s = re.sub(r'<.*?>','',s)
	s = re.sub(r'(\s*\\[rn]\s*)+','\n\n',s)
	return s

####################

def dirname_to_docs(dirname):
	ret = {}
	for subdirname in os.listdir(dirname): #{country}-annot{n}
		if os.path.isdir(os.path.join(dirname,subdirname)):
			#country = subdirname.split('-')[0]
			ret[subdirname] = {}
			for filename in os.listdir(os.path.join(dirname,subdirname,'3-txt')):
				if os.path.isfile(os.path.join(dirname,subdirname,'3-txt',filename)):
					doc = filename.split('.')[0]
					#ret[subdirname+'_'+filename.split('.')[0]] = filename_to_doc(os.path.join(dirname,subdirname,'3-txt',filename))
					#ret['_'.join([country,doc])] = filename_to_doc(os.path.join(dirname,subdirname,'3-txt',filename))
					ret[subdirname][filename.split('.')[0]] = filename_to_doc(os.path.join(dirname,subdirname,'3-txt',filename))

#	for filename in os.listdir(dirname):
#		if os.path.isfile(os.path.join(dirname,filename)):
#			ret[filename.split('.')[0]] = filename_to_doc(os.path.join(dirname,filename))

	return ret

def filename_to_doc(filename):
	try:
		#with open(filename, 'r', encoding='utf-8') as f:
		with open(filename, 'r', encoding='latin-1') as f:
			return list(filter(None,[line_to_sentences(line.strip()) for line in f.readlines()]))
	except Exception as err:
		print(err)

def line_to_sentences(line):
	#sentences = list(filter(None, [sent.strip().split() for sent in re.split('(\.|\!|\?)',line)]))
	#return list(filter(None, [sent.strip().split() for sent in re.split('\.|\!|\?',line)]))
	ret = []
	#for sent in re.split('\.|\!|\?',line):
	for sent in nltk.tokenize.sent_tokenize(line.strip()):
		cleansent = remove_html(sent.strip()).strip()
		if len(cleansent):
			toks = nltk.tokenize.word_tokenize(cleansent)
			postoks = nltk.pos_tag(toks)
			chunker = nltk.RegexpParser(grammar)
			tree = chunker.parse(postoks)
			ret.append({'tok':toks, 'pos':postoks, 'tree':tree})
	return ret

####################

@contextmanager
def writeopen(outputfilename=None):
	#if len(outputfilename) > 0: outputfile = open(outputfilename, 'w', encoding='utf-8')
	if len(outputfilename) > 0: outputfile = open(outputfilename, 'w', encoding='latin-1')
	else: outputfile = sys.stdout
	try: yield outputfile
	finally:
		if outputfile is not sys.stdout: outputfile.close()

def print_docs_to_filename(annots, filename):
	try:
		with writeopen(filename) as outputfile:
			print('{', file=outputfile)
			for annot in annots:
				print(('\t'*1)+'"'+annot+'" :', file=outputfile)
				print(('\t'*2)+'{', file=outputfile)
				for doc in annots[annot]:
					print(('\t'*3)+'"'+doc+'" :', file=outputfile)
					print(('\t'*4)+'[', file=outputfile)
					for line in annots[annot][doc]:
						print(('\t'*5)+'[', file=outputfile)
						for sent in line:
							print(('\t'*6)+'{', file=outputfile)
							print(('\t'*7), '"tok" :', sent['tok'], file=outputfile)
							print(('\t'*7), '"pos" :' , sent['pos'], file=outputfile)
							print(('\t'*7), '"tree" :', ' '.join(str(sent['tree']).split()), file=outputfile)
							print(('\t'*6)+'}', file=outputfile)
						print(('\t'*5)+']', file=outputfile)
					print(('\t'*4)+']', file=outputfile)
				print(('\t'*2)+'}', file=outputfile)
			print('}', file=outputfile)
	except Exception as err:
		print(err)

####################

