
import sys, nltk, numpy
from contextlib import contextmanager

####################

# { 'annot1' : { 'Statue': {'d2' : {'rank' : '9/10', 'desc' : [], 'category': '' } } } }

def generate_description_model(annots, entities, model_dir):
#	for annot in annots:
#		for doc in annots[annot]:
#			print(annot, doc)
#			for line in annots[annot][doc]:
#				for sent in line:
#					all_phrases_with_label(sent['tree'],'NP')
	desc = {}
	model = {}
	for annot in entities:
		desc[annot] = {}
		for attraction in entities[annot]:
			#print(annot, attraction, entities[annot][attraction][0].split(';'))
#			print('\n', annot, attraction, entities[annot][attraction])
			for doc in entities[annot][attraction]['desc']:
				desc[annot][doc] = []
#				print('GOLD:', entities[annot][attraction]['desc'][doc][0].split(';'))
				if annot in annots and doc in annots[annot]:
					#for line in annots[annot][doc]:
					for line in get_lines_about_attraction(attraction.strip(), [key.strip() for key in entities[annot].keys()], annots[annot][doc]):
						for sent in line:
							#all_subtrees_with_label(sent['tree'],'NP')
							desc[annot][doc] += [x for x in all_phrases_with_label(sent['tree'],'NP') if len(x.split()) > 1 and not attraction in x and x not in entities[annot]]
				for d in desc[annot][doc]:
					yay = (d in [x.strip() for x in entities[annot][attraction]['desc'][doc][0].split(';')])
					for gram in [' '.join(x) for x in list(nltk.ngrams(d.lower().split(), 1))]+[' '.join(x) for x in list(nltk.ngrams(d.lower().split(), 2))]+[' '.join(x) for x in list(nltk.ngrams(d.lower().split(), 3))]:
						if gram in model:
							model[gram]['yay'] += 1 if yay else 0
							model[gram]['nay'] += 0 if yay else 1
						else: model[gram] = {'yay':(1 if yay else 0), 'nay':(0 if yay else 1)}

	for gram in model:
		model[gram]['prob'] = model[gram]['yay'] / (model[gram]['yay']+model[gram]['nay'])

	if model_dir[-1] is '/': model_dir = model_dir[:-1]
	print_model_to_filename(model, model_dir+'/description.model')

#####

def add_descriptions_to_attractions(annots, attractions, model_dir):
	if model_dir[-1] is '/': model_dir = model_dir[:-1]
	model = model_from_filename(model_dir+'/description.model')
	for annotator in attractions:
		for attraction in attractions[annotator]:
			for doc in attractions[annotator][attraction]:
				attractions[annotator][attraction][doc]['desc'] = []
				if annotator in annots and doc in annots[annotator]:
					#print(attractions[annotator])
					#for line in get_lines_about_attraction_test(attractions[annotator][attraction][doc]['instances']['line'], [y for y in [attractions[annotator][x][doc]['instances']['line'] if doc in attractions[annotator][x] else -1 for x in attractions[annotator] if x is not attraction] if y is not -1], annots[annotator][doc]):
					for line in get_lines_about_attraction(attraction.strip(), [key.strip() for key in attractions[annotator].keys()], annots[annotator][doc]):
						for sent in line:
							attractions[annotator][attraction][doc]['desc'] += [x for x in all_phrases_with_label(sent['tree'],'NP') if len(x.split()) > 1 and not attraction in x and x not in attractions[annotator] and calc_prob_of_phrase(model,x) > 0]
	#print(attractions)
	#for attraction in attractions:
	#	attractions[attraction]['descriptions'] = annots_and_instances_to_descriptions(annots,attractions[attraction]['instances'])
	return attractions

####################

def calc_prob_of_phrase(model, phrase):
	probs = []
	for gram in [' '.join(x) for x in list(nltk.ngrams(phrase.lower().split(), 1))]+[' '.join(x) for x in list(nltk.ngrams(phrase.lower().split(), 2))]+[' '.join(x) for x in list(nltk.ngrams(phrase.lower().split(), 3))]:
		if gram in model: probs.append(model[gram])
	return (numpy.mean(probs) if len(probs) else 1)

def model_from_filename(filename):
	try:
		#with open(filename, 'r', encoding='utf-8') as f:
		with open(filename, 'r', encoding='latin-1') as f:
			model = {}
			for line in f:
				gram, prob = line.strip().split('\t')
				prob = float(prob)
				model[gram] = prob
			return model
	except Exception as err:
		print(err)

def get_lines_about_attraction(this_attraction, attractions, lines):
	for i, line in enumerate(lines):
		text = ' '.join([' '.join(sent['tok']) for sent in line])
		if this_attraction in text:
			return lines[i:min(len(lines),i+2)]
	return []

def get_lines_about_attraction_test(this_attraction, attractions, lines):
#	begin = this_attraction
#	end = this_attraction+1
#	print(sorted(attractions+[this_attraction]))
#	for i, attraction in enumerate(sorted(attractions+[this_attraction])):
#		if attraction is this_attraction and i+1 < len(attractions):
#			end = attraction
#			break
#	print(lines[begin:end])
#	return lines[begin:end]
	return lines[this_attraction:min(len(lines),this_attraction+2)]

def get_lines_about_attraction_train(this_attraction, attractions, lines):
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
				#print('!!!!!', text)
				return lines[begin:end]
			else:
				begin = 0
				end = 0
				we_in_dere = False
	return lines[begin:end]

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
	#print(ret)
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
			for gram in model:
				print(gram+'\t'+str(model[gram]['prob']), file=outputfile)
	except Exception as err:
		print(err)

####################

