import nltk

# look for rank
# look for word shape

"""
{ 'annot1' : { 'Statue': {'d2' : {'rank' : '9/10', 'desc' : [], 'category': '' } } } }
"""


####################

def docs_to_named_entities(docs):
        grammar = "RANKED: {<CD><DT>*<NNP><NN.*>*<PP>*<NN.*>*}"
        chunker = nltk.RegexpParser(grammar)
        ret = {} 
        for annot in docs:
                ret[annot] = {}
                for doc in docs[annot]:
                        attractions = []
                        for i, line in enumerate(docs[annot][doc]):
                                for j, sent in enumerate(line):
                                        tree = chunker.parse(sent['pos'])
                                        for subtree in tree.subtrees():
                                                if subtree.label() == 'RANKED':
                                                        print(doc, subtree)
                # ret[annot][entity] = {}
                # ret[annot][entity][doc] = {}
                # ret[annot][entity][doc]['rank'] = N 
                # ret[annot][entity][doc]['desc'] = '' 
                # ret[annot][entity][doc]['category'] = N 
                # ret[annot][entity][doc]['instances'] = []
        return ret

####################

