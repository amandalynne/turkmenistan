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

def docs_and_entities_to_attractions(docs, entities):
	ret = {}

	names_and_instances = docs_and_entities_to_instances(docs, entities)
	for name in names_and_instances:
		ret[name] = {}
		ret[name]['category'] = instances_to_category(names_and_instances[name])
		ret[name]['instances'] = names_and_instances[name]

	return ret

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

def initialize_dataframe(tokens,columns):
    '''
    This function initializes the output dataframe.
    '''
    data = np.zeros(len(tokens), len(columns))
    return pd.DataFrame(data, index=tokens, columns=category_list)


def docs_and_entities_to_instances(docs, entities):
	return {'Generic Attraction Name':[{ 'indices':['x',0,0,[0,0]], 'string':'Generic Attraction Name Variant', 'category':'other', 'rank':0 }]}

def instances_to_category(instances):
	df = pd.DataFrame(index=tokens, columns=category_list)
	return 'other'

####################
