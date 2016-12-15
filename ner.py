import nltk
import re

"""
{ 'annot1' : { 'Statue': {'d2' : {'rank' : '9/10', 'desc' : [], 'category': '' } } } }
"""

# If an attraction candidate contains one of these words,
# it is BOGUS. Take it off the list!
NONO_WORDS = ['Prev', 'Login', 'September', 'October', 'November', 'December']



####################

def postprocess_attr_list(attractions):
        """ filter out bad shit and order it """
        ret = []
        for attr in attractions:
            ret.append((int(attr[0]), ' '.join(attr[1:])))
        ret = list(set(ret))
        ret = sorted(ret, key = lambda x: x[0])
        #while ret[-1][0] > len(ret):
        while len(ret) and len(ret[-1]) and ret[-1][0] > len(ret):
            ret.pop()
        for attr in ret:
            if attr[1] in NONO_WORDS:
                ret.remove(attr) 
        #if ret[-1][0] != 0:
        if len(ret) and len(ret[-1]) and ret[-1][0] != 0:
            new_ret = []
            for attr in ret:
                if attr[0] != 0:
                    new_ret.append(attr)
            ret = new_ret
        return ret


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
                        chunks = []
                        for i, line in enumerate(docs[annot][doc]):
                                for j, sent in enumerate(line):
                                        tree = chunker.parse(sent['pos'])
                                        for subtree in tree.subtrees():
                                                    chunk = ''
                                                    if subtree.label() == 'RANKED':
                                                            chunk = [x[0] for x in subtree.leaves()]
                                                            if re.match(digit_pattern, chunk[0]):
                                                                    chunks.append(chunk)
                                                    elif subtree.label() == 'UNRANKED':
                                                            if re.match(digit_pattern, line[0]['tok'][0]):
                                                                    rank = line[0]['tok'][0]
                                                                    chunk = [x[0] for x in subtree.leaves()]
                                                                    chunk.insert(0, line[0]['tok'][0])
                                                                    chunks.append(chunk) 
                                                            elif j == 0 and subtree.label() == 'UNRANKED':
                                                                    chunk = [x[0] for x in subtree.leaves()]
                                                                    chunk.insert(0, '0') 
                                                                    chunks.append(chunk)
                                                    entity = ' '.join(chunk[1:])
                                                    ret[annot][entity] = {}
                                                    ret[annot][entity][doc] = {}
                                                    ret[annot][entity][doc]['instances'] = {}
                                                    ret[annot][entity][doc]['instances']['line'] = i
                                                    ret[annot][entity][doc]['instances']['sent'] = j 
                        #print(annot, doc, postprocess_attr_list(doc_attractions))
                        attractions = postprocess_attr_list(chunks)
                        for attr in attractions:
                                entity = attr[1]
                                rank = "{0}/{1}".format(attr[0], len(attractions))
                                ret[annot][entity][doc]['rank'] = rank 
                                ret[annot][entity][doc]['desc'] = '' 
                                ret[annot][entity][doc]['category'] = '' 
        return ret


####################

