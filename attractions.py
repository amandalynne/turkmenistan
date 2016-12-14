"""
attractions.py
-----------
This script is generates the attraction category for a given data structure.
"""
####################
####Libraries#####
import sys
import pandas as pd
import numpy as np
import nltk

####################
##Global Variables##
category_list = ["amusement park", "aquarium",
        "archaeological site", "architecture", "art", "beach",
	"bridge", "building","canyon", "casino", "castle",
	"cave", "ceremony", "church", "city", "city district",
	"city/town square", "cliff", "coast", "desert", "fair",
	"festival", "forest", "fort", "fountain", "game reserve",
	"gallery", "garden", "glacier", "hotel", "historic site",
	"island", "lake", "market", "memorial", "monument",
	"mosque", "mountain", "mountain peak", "museum", "nature",
	"nature reserve", "national park", "ocean", "palace",
	"park", "prison", "region", "resort", "river", "ruin",
	"school", "shopping mall", "show", "stadium", "temple",
	"theatre", "tower", "town", "trail", "waterfront",
	"waterfall", "viewpoint", "zoo"];
####################

def docs_and_entities_to_attractions(docs, entities):
	training(entities)
	return entities
	#ret = {}

	#names_and_instances = docs_and_entities_to_instances(docs, entities)
	#for name in names_and_instances:
	#	ret[name] = {}
	#	ret[name]['category'] = instances_to_category(names_and_instances[name])
	#	ret[name]['instances'] = names_and_instances[name]

	#return ret

#####################

def initialize_dataframe(tokens,columns):
    '''
    This function initializes the output dataframe.
    '''
    data = np.zeros(len(tokens), len(columns))
    return pd.DataFrame(data, index=tokens, columns=category_list)

def token_list_generator(entities):
	token_category = dict()
	for annot in entities:
		for entity in annot:
			for description in entity:
				for doc in description:
					if string[1] in token_category:
						token_category[string[1]] = token_category[string[1]] + string[0].split("; ")
					else:
						token_category[string[1]] = string[0].split("; ")
	return token_category

def type_generator(tcd):
	return set([item for sublist in l for item in tcd.values()])

def df_filler(df,tcd):
	for category,words in tcd.iteritems():
		for w in words:
			df[category][w] += 1.0
	return df

def count_to_probabilty(df,tcd_keys):
	for c in tcd_keys:
		df[c].divide(len(tcd_keys))
	return df

#def docs_and_entities_to_instances(docs, entities):
	#return {'Generic Attraction Name':[{ 'indices':['x',0,0,[0,0]], 'string':'Generic Attraction Name Variant', 'category':'other', 'rank':0 }]}

def training(entities):
	tcd = token_list_generator(entities)
	tokens = type_generator(tcd)
	tcd_keys = tcd.keys()
	df = count_to_probabilty(df_filler(pd.DataFrame(index=tokens, columns=category_list),tcd),tcd_keys)
	df.to_csv('./model-dir/attractions.model', sep='\t')
	return 'other'

####################
