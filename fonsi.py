#!/usr/bin/python2.7
"""
fonsi.py
-----------
This script is generates the attraction category for a given cateogry.
"""
import sys
import pandas as pd
import numpy as np
import nltk

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

def initialize_dataframe(tokens,columns):
    '''
    This function initializes the output dataframe.
    '''
    data = np.zeros(len(tokens), len(columns))
    return pd.DataFrame(data, index=tokens, columns=category_list)

def main(args):
    df = pd.DataFrame(index=tokens, columns=category_list)
    print category_list

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="This script is generates the"
						 "attraction category for a"
						 "given cateogry.")
    argv = parser.parse_args()
    sys.exit(main(args=argv))
