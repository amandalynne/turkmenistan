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
import re

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

def docs_and_entities_to_attractions(docs, entities,train):
	if train:
		training(entities)
	else:
		entities = testing(docs)
	return entities

#####################

def initialize_dataframe(tokens,columns):
	'''
	This function initializes the output dataframe.
	'''
	data = np.zeros((len(tokens), len(columns)))
	return pd.DataFrame(data, index=tokens, columns=columns)

def cleaner(entry):
    return re.sub('[^A-Za-z0-9 ]+', '', entry).lower().split()

def token_list_generator(entities):
	token_category = dict()
	for annot in entities:
		for entity in entities[annot]:
			for description in entities[annot][entity]:
				for doc in entities[annot][entity]['desc']:
					entry = entities[annot][entity]['desc'][doc]
					if "; " in entry[1]:
						entry_split = entry[1].split("; ")
						for e in entry_split:
							if e[1] in category_list:
								if e[1] in token_category:
									token_category[e[1]] = token_category[e[1]] + cleaner(e[0])
								else:
									token_category[e[1]] = cleaner(e[0])
					else:
						if entry[1] in category_list:
							if entry[1] in token_category:
								token_category[entry[1]] = token_category[entry[1]] + cleaner(entry[0])
							else:
								token_category[entry[1]] = cleaner(entry[0])
	return token_category

def type_generator(tcd):
	return set([item for sublist in tcd.values() for item in sublist])

def df_filler(df,tcd):
	for category,words in tcd.items():
		for w in words:
			if df[category][w]:
				df[category][w] += 1.0
			else:
				df[category][w] = 1.0
	return df

def count_to_probabilty(df):
	return df.divide(len(df.columns))

#def docs_and_entities_to_instances(docs, entities):
	#return {'Generic Attraction Name':[{ 'indices':['x',0,0,[0,0]], 'string':'Generic Attraction Name Variant', 'category':'other', 'rank':0 }]}

def training(entities):
	tcd = token_list_generator(entities)
	tokens = type_generator(tcd)
	df = count_to_probabilty(df_filler(initialize_dataframe(tokens, category_list),tcd))
	df.to_csv('./model-dir/attractions.model', sep='\t')
	return 'Complete'

def testing(entities):
	tcd = token_list_generator(entities)
	tokens = type_generator(tcd)
	df = count_to_probabilty(df_filler(initialize_dataframe(tokens, category_list),tcd))
	df.to_csv('./model-dir/attractions.model', sep='\t')
	return

####################
