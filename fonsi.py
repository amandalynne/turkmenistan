#!/usr/bin/python2.7
"""
fonsi.py
-----------
This script is generates the attraction category for a given cateogry.
"""
import sys

################################Score_Dict######################################
#The template for storing scoring information#
score_dict = {"amusement park": 0.0,        "aquarium": 0.0,
              "archaeological site": 0.0,   "architecture": 0.0,
              "art": 0.0,                   "beach": 0.0,
              "bridge": 0.0,                "building": 0.0,
              "canyon": 0.0,                "casino": 0.0,
              "castle": 0.0,                "cave": 0.0,
              "ceremony": 0.0,              "church": 0.0,
              "city": 0.0,                  "city district": 0.0,
              "city/town square": 0.0,      "cliff": 0.0,
              "coast": 0.0,                 "desert": 0.0,
              "fair": 0.0,                  "festival": 0.0,
              "forest": 0.0,                "fort": 0.0,
              "fountain": 0.0,              "game reserve": 0.0,
              "gallery": 0.0,               "garden": 0.0,
              "glacier": 0.0,               "hotel": 0.0,
              "historic site": 0.0,         "island": 0.0,
              "lake": 0.0,                  "market": 0.0,
              "memorial": 0.0,              "monument": 0.0,
              "mosque": 0.0,                "mountain": 0.0,
              "mountain peak": 0.0,         "museum": 0.0,
              "nature": 0.0,                "nature reserve": 0.0,
              "national park": 0.0,         "ocean": 0.0,
              "palace": 0.0,                "park": 0.0,
              "prison": 0.0,                "region": 0.0,
              "resort": 0.0,                "river" : 0.0,
              "ruin": 0.0,                  "school": 0.0,
              "shopping mall": 0.0,         "show": 0.0,
              "stadium": 0.0,               "temple": 0.0,
              "theatre": 0.0,               "tower": 0.0,
              "town": 0.0,                  "trail": 0.0,
              "waterfront": 0.0,            "waterfall": 0.0,
              "viewpoint": 0.0,             "zoo": 0.0
              };

def main(args):
    print score_dict

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="This script is generates the attraction category for a given cateogry.")
    argv = parser.parse_args()
    sys.exit(main(args=argv))
