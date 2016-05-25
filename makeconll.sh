#!/bin/bash

for set in *.txt; do
    cat $set | ./conllize.sh > $(basename $set .txt).conll
done
