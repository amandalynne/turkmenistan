#!/bin/sh

python3 test.py $1 $2 $3
python3 make_summary.py $3
