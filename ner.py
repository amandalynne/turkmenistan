
####################

def docs_to_named_entities(docs):
	ret = []
	for doc in docs:
		for i, line in enumerate(docs[doc]):
			for j, sentence in enumerate(line):
				for k, tok in enumerate(sentence):
					ret.append( [ [doc,i,j,k], tok, 'Generic Attraction Name' ] )
	return ret

####################

