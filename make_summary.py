import sys
import os
import re

from collections import defaultdict
from operator import itemgetter

"""
Produces a summary.out file
Currently doesn't take arguments, but will take a directory of files.
"""


class Attraction:
    def __init__(self, name, rank, cats, desc, doc):
        self.name = name
        self.rank = rank
        self.cats = cats
        self.desc = desc 
        self.doc = doc 
        

    def __repr__(self):
        return self.name

    def score_m(self):
        TOTAL_DOCS = 5
        

    def score_r(self):
        if self.rank[0] == '0':
            score_r = 0.5
        else:
            score_r = self.rank 
    
    def avg_score(self):
        score_m = self.score_m()
        score_r = self.score_r()
        return (score_m + score_r) / 2

    def print_summary(self):
        print "  %{0} {1} {2} {3} {4}".format(self.doc, self.rank, self.name, self.cats, self.desc)

ATTRACTION_LIST = []
ATTRACTION_DICT = defaultdict(list)

## rank  attraction ##cats %%desc
def process_file(filename):
    line_pattern = r'^\s*(\d+)\s+([^#]+)\s+(##[^%]+)\s+(%%.*)$'
    linecount = str(sum(1 for line in open(filename))) 
    with open(filename, 'r') as inf:
        for line in inf.readlines(): 
            match = re.match(line_pattern, line.strip())
            rank = "{0}/{1}".format(match.group(1), linecount)
            name = match.group(2)
            cats = match.group(3)
            desc = match.group(4)
            doc = filename[:2]
            ATTRACTION_LIST.append(Attraction(name, rank, cats, desc, doc)) 
           
def find_overlaps():
    attr_set = set(ATTRACTION_LIST)
    for attr in attr_set:
        ATTRACTION_DICT[attr.name]
    for attr in ATTRACTION_LIST:
        ATTRACTION_DICT[attr.name].append(attr)
   
def score_R(attr):
    avg = 0
    for instance in ATTRACTION_DICT[attr]:
        rank = float(instance.rank[0])
        total = float(instance.rank[-1])
        if rank == 0:
            avg += 0 
        else:
            avg += (rank/total)
    if avg == 0:
        score_r = 0.5
    else:
        score_r = 1 - (avg/len(ATTRACTION_DICT[attr])) 
    return score_r

 
def score():
    scored = []
    for attr in ATTRACTION_DICT.keys():
        if len(ATTRACTION_DICT[attr]) == 1:
            score_m = float(1)/5
        else:
            score_m = len(ATTRACTION_DICT[attr]) / float(5) 
        score_r = score_R(attr) 
        avg_score = (score_m + score_r) / 2
        output = [attr, score_m, score_r, avg_score]
        scored.append(output)
    scored.sort(key = lambda x:x[-1], reverse=True)
    return scored 

def print_summary():
    for i, scores in enumerate(score()):
        attr = scores[0]
        score_m = str(scores[1])
        score_r = str(scores[2])
        avg_score = str(scores[3])
        top_line = "{0} {1} {2} {3} {4}".format(i+1, attr, score_m, score_r, avg_score)
        if i+1 > 1:
            print "\n{0}".format(top_line)
        else:
            print top_line
        for a in ATTRACTION_DICT[attr]:
            a.print_summary()          

if __name__ == "__main__":
    for filename in os.listdir(os.curdir):
        if filename.startswith('d'):
            process_file(filename)
    find_overlaps()
    print_summary()
