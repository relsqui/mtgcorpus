#!/bin/bash

for set in *.json; do
    echo "$set ..." >&2
    # unix2dos converts line endings for the sake of Windows-based concordancers
    # it's in the dos2unix package (named for the opposite tool)
    cat $set | ./mtgcorpus.py | unix2dos > $(basename $set .json).txt
done
echo "done" >&2
