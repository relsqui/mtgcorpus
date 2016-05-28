#!/usr/bin/python

import sys
import pprint

def eprint(text):
    sys.stderr.write(text + "\n")

# grab all the data from stdin
data = sys.stdin.read().splitlines()

# print the file description comments to stderr
for line in (data[:4]):
    eprint(line)

# set up variables to read cards into
cards = []
card = {}
card["lines"] = []
line = []
# used for tracking where we are in the card, see below
meta_next = False

# chew through all the lines
for d in data[4:]:
    if not d:
        # blank means we're done with the line we were reading
        if len(line):
            # it might be empty if the last line was blank too
        card["lines"].append(line)
        line = []
    elif d[0] is "#":
        if meta_next:
            # we just saw a name, this is metadata
            card["meta"] = d
            card["lines"] = []
            meta_next = False
        else:
            # the beginning of a new card
            if card["lines"]:
                cards.append(card)
            card = {}
            card["name"] = d
            # we should see a cost/type line next
            meta_next = True
    else:
        # just another token, append to the line
        line.append(tuple(d.split("\t")))

pprint.pprint(cards[1])
