
import sys, nltk
from contextlib import contextmanager

####################

def generate_description_model(annots, entities, model_dir):
#	for annot in annots:
#		for doc in annots[annot]:
#			print(annot, doc)
#			for line in annots[annot][doc]:
#				for sent in line:
#					all_phrases_with_label(sent['tree'],'NP')
	for annot in entities:
		for attraction in entities[annot]:
			#print(annot, attraction, entities[annot][attraction][0].split(';'))
			print('\n', annot, attraction, entities[annot][attraction])
			for doc in entities[annot][attraction]['desc']:
				print('GOLD:', entities[annot][attraction]['desc'][doc][0].split(';'))
				if annot in annots and doc in annots[annot]:
					#for line in annots[annot][doc]:
					for line in get_lines_about_attraction(attraction.strip(), [key.strip() for key in entities[annot].keys()], annots[annot][doc]):
						print('--')
						for sent in line:
							#all_subtrees_with_label(sent['tree'],'NP')
							all_phrases_with_label(sent['tree'],'NP')

	model = [['thing1', 'thing2'],[.5, .5]]

	if model_dir[-1] is '/': model_dir = model_dir[:-1]
	print_model_to_filename(model, model_dir+'/description.model')

def get_lines_about_attraction(this_attraction, attractions, lines):
	begin = 0
	end = 0
	we_in_dere = False
	# first instance of attraction in line is this_attraction = begin
	# first instance of attraction in line is other_attraction = end
	# else pass
	for i, line in enumerate(lines):
		#text = ' '.join([' '.join(sent['tok']) for sent in line])
		text = ''.join([''.join(sent['tok']) for sent in line])
		this_instance = (text.index(this_attraction) if this_attraction in text else -1)
		#contains_other = any([(x in text and x is not this_attraction) for x in attractions])
		other_instances = [z for z in [(text.index(x) if x in text and x is not this_attraction else -1) for x in [''.join(y.split()) for y in attractions]] if z is not -1]
		if this_instance >= 0 and (not len(other_instances) or this_instance < min(other_instances)):
			if not we_in_dere:
				begin = i
				we_in_dere = True
		elif we_in_dere and len(other_instances) and (this_instance < 0 or min(other_instances) < this_instance):
			if i > begin+1:
				end = i
				print('!!!!!', text)
				return lines[begin:end]
			else:
				begin = 0
				end = 0
				we_in_dere = False
	return lines[begin:end]

def add_descriptions_to_attractions(annots, attractions):
	for attraction in attractions:
		attractions[attraction]['descriptions'] = annots_and_instances_to_descriptions(annots,attractions[attraction]['instances'])
	return attractions

####################

def annots_and_instances_to_descriptions(annots, instances):
	return [{ 'indices':['x',0,0,[0,0]], 'string':'a generic description' }]

def tree_to_phrase(tree):
	return ' '.join([leaf[0] for leaf in tree.leaves()]).replace(' ,',',')

def all_subtrees_with_label(tree, label):
	ret = []
	for subtree in tree.subtrees(filter = lambda t: t.label()==label):
		s = tree_to_phrase(subtree)
		if not any([(s is not thing and s in thing) for thing in ret]):
			ret.append(subtree)
	#print(ret)
	return ret

def all_phrases_with_label(tree, label):
	ret = []
	for subtree in tree.subtrees(filter = lambda t: t.label()==label):
		s = tree_to_phrase(subtree)
		if not any([(s is not thing and s in thing) for thing in ret]):
			ret.append(s)
	print(ret)
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

def print_model_to_filename(model, filename):
	try:
		with writeopen(filename) as outputfile:
			for line in model:
				print('\t'.join([str(item) for item in line]), file=outputfile)
	except Exception as err:
		print(err)

####################

