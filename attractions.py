
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

def docs_and_entities_to_instances(docs, entities):
	return {'Generic Attraction Name':[{ 'indices':['x',0,0,[0,0]], 'string':'Generic Attraction Name Variant', 'category':'other', 'rank':0 }]}

def instances_to_category(instances):
	return 'other'

####################
