import nltk
import re

"""
{ 'annot1' : { 'Statue': {'d2' : {'rank' : '9/10', 'desc' : [], 'category': '' } } } }
"""

# If an attraction candidate contains one of these words,
# it is BOGUS. Take it off the list!
NONO_WORDS = ['Prev', 'Login']



####################

def docs_to_named_entities(docs):
        grammar = """
                    RANKED: {<CD><DT>*<JJ>*<NNP><NN.*>*<PP>*<NN.*>*}
                    UNRANKED: {<DT>*<JJ>*<NNP><NN.*>*<PP>*<NN.*>*}
                    """
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
                                                elif subtree.label() == 'UNRANKED':
                                                        if re.match(digit_pattern, line[0]['tok'][0]):
                                                                rank = line[0]['tok'][0]
                                                                chunk = [x[0] for x in subtree.leaves()]
                                                                chunk.insert(0, line[0]['tok'][0])
                                                                doc_attractions.append(chunk) 
                                                        elif j == 0 and subtree.label() == 'UNRANKED':
                                                                chunk = [x[0] for x in subtree.leaves()]
                                                                chunk.insert(0, '0') 
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

