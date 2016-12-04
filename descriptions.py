
####################

def add_descriptions_to_attractions(docs, attractions):
	for attraction in attractions:
		attractions[attraction]['descriptions'] = docs_and_instances_to_descriptions(docs,attractions[attraction]['instances'])
	return attractions

####################

def docs_and_instances_to_descriptions(docs, instances):
	return [{ 'indices':['x',0,0,[0,0]], 'string':'a generic description' }]

####################
