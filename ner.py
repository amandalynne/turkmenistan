import nltk
import re

"""
{ 'annot1' : { 'Statue': {'d2' : {'rank' : '9/10', 'desc' : [], 'category': '' } } } }
"""


####################

def docs_to_named_entities(docs):
        grammar = "RANKED: {<CD><DT>*<JJ>*<NNP><NN.*>*<PP>*<NN.*>*}"
        chunker = nltk.RegexpParser(grammar)
        digit_pattern = r'^\d+$'
        ret = {}
        for annot in docs:
                annot_attractions = []
                ret[annot] = {}
                for doc in docs[annot]:
                        doc_attractions = []
                        for i, line in enumerate(docs[annot][doc]):
                                for j, sent in enumerate(line):
                                        tree = chunker.parse(sent['pos'])
                                        for subtree in tree.subtrees():
                                                if subtree.label() == 'RANKED':
                                                        chunk = [x[0] for x in subtree.leaves()]
                                                        if re.match(digit_pattern, chunk[0]):
                                                                doc_attractions.append(chunk)
                        print(annot, doc, doc_attractions)
                # ret[annot][entity] = {}
                # ret[annot][entity][doc] = {}
                # ret[annot][entity][doc]['rank'] = N 
                # ret[annot][entity][doc]['desc'] = '' 
                # ret[annot][entity][doc]['category'] = N 
                # ret[annot][entity][doc]['instances'] = []
        return ret


####################

