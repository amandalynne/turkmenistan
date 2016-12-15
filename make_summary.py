import sys
import os
import re

from collections import defaultdict
from operator import itemgetter

"""
Produces a summary.out file from d*.out files.
Takes a directory of files.
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
        return "\n  %{0} {1} {2} {3} {4}".format(self.doc, self.rank, self.name, self.cats, self.desc)


## rank  attraction ##cats %%desc
def process_file(filename, attr_list):
    line_pattern = r'^\s*(\d+)\s+([^#]+)\s+(##[^%]+)\s+(%%.*)$'
    linecount = str(sum(1 for line in open(filename))) 
    with open(filename, 'r') as inf:
        for line in inf.readlines(): 
            match = re.match(line_pattern, line.strip())
            rank = "{0}/{1}".format(match.group(1), linecount)
            name = match.group(2)
            cats = match.group(3)
            desc = match.group(4)
            doc = filename[-6:-4]
            attr_list.append(Attraction(name, rank, cats, desc, doc)) 
           
def find_overlaps(attr_list, attr_dict):
    attr_set = set(attr_list)
    for attr in attr_set:
        attr_dict[attr.name]
    for attr in attr_list:
        attr_dict[attr.name].append(attr)
   
def score_R(attr, attr_dict):
    avg = 0
    for instance in attr_dict[attr]:
        pattern = r'(\d+)/(\d+)'
        rank_match = re.match(pattern, instance.rank)
        rank = float(rank_match.group(1))
        total = float(rank_match.group(2)) 
        if rank == 0:
            avg += 0 
        else:
            avg += (rank/total)
    if avg == 0:
        score_r = 0.5
    else:
        score_r = 1 - (avg/len(attr_dict[attr])) 
    return score_r

 
def score(attr_dict):
    scored = []
    for attr in list(attr_dict.keys()):
        if len(attr_dict[attr]) == 1:
            score_m = float(1)/5
        else:
            score_m = len(attr_dict[attr]) / float(5) 
        score_r = score_R(attr, attr_dict) 
        avg_score = (score_m + score_r) / 2
        output = [attr, score_m, score_r, avg_score]
        scored.append(output)
    scored.sort(key = lambda x:x[-1], reverse=True)
    return scored 

def print_summary(attr_dict, output_dir):
    if os.path.isfile(os.path.join(output_dir, "summary.out")):
        os.remove(os.path.join(output_dir, "summary.out"))
    with open(os.path.join(output_dir, "summary.out"), 'a+') as f:
        for i, scores in enumerate(score(attr_dict)):
            attr = scores[0]
            score_m = str(scores[1])
            score_r = str(scores[2])
            avg_score = str(scores[3])
            top_line = "{0} {1} {2} {3} {4}".format(i+1, attr, score_m, score_r, avg_score)
            if i+1 > 1:
                f.write("\n{0}".format(top_line))
            else:
                f.write(top_line)
            for a in sorted(set(attr_dict[attr])):
                f.write(a.print_summary()) 

if __name__ == "__main__":
    output_dir = sys.argv[1]
    for annot in os.listdir(output_dir):
        attr_list = [] 
        attr_dict = defaultdict(list) 
        d_output_dir = os.path.join(output_dir, annot, '4-output')
        for filename in os.listdir(d_output_dir):
            if filename.startswith("d"):
                process_file(os.path.join(d_output_dir, filename), attr_list)
            find_overlaps(attr_list, attr_dict)
            print_summary(attr_dict, d_output_dir)
