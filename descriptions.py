
import nltk

####################

def generate_description_model(annots, entities):
#	for annot in annots:
#		for doc in annots[annot]:
#			print(annot, doc)
#			for line in annots[annot][doc]:
#				for sent in line:
#					all_phrases_with_label(sent['tree'],'NP')
	for annot in entities:
		for attraction in entities[annot]:
			print(annot, attraction, entities[annot][attraction])
			for doc in entities[annot][attraction]['desc']:
				if annot in annots and doc in annots[annot]:
					for line in annots[annot][doc]:
						for sent in line:
							all_phrases_with_label(sent['tree'],'NP')

def add_descriptions_to_attractions(annots, attractions):
	for attraction in attractions:
		attractions[attraction]['descriptions'] = annots_and_instances_to_descriptions(annots,attractions[attraction]['instances'])
	return attractions

####################

def annots_and_instances_to_descriptions(annots, instances):
	return [{ 'indices':['x',0,0,[0,0]], 'string':'a generic description' }]

def all_phrases_with_label(tree, label):
	ret = []
	for subtree in tree.subtrees(filter = lambda t: t.label()==label):
		#print(' '.join([leaf[0] for leaf in subtree.leaves()]))
		s = ' '.join([leaf[0] for leaf in subtree.leaves()])
		if not any([(s is not thing and s in thing) for thing in ret]):
			ret.append(s)
	print(ret)

####################
