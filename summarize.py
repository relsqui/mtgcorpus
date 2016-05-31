#!/usr/bin/python

import sys
import pprint

def eprint(text):
    sys.stderr.write(text + "\n")

# grab all the data from stdin
data = sys.stdin.read().splitlines()

# set up variables to read cards into
cards = []
card = {}
card["lines"] = []
line = []
# used for tracking where we are in the card, see below
meta_next = False
cards_by_syntax = {}

# chew through all the lines
for d in data:
    if not d:
        # blank means we're done with the line we were reading
        if len(line):
            # it might be empty if the last line was blank too
            card["lines"].append(line)
            # index 4 is the language-specific part of speech
            key = tuple(l[4] for l in line)
            if key in cards_by_syntax:
                cards_by_syntax[key].append(card["name"])
            else:
                cards_by_syntax[key] = [card["name"]]
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
            # strip the initial # from the name
            card["name"] = d[1:]
            # we should see a cost/type line next
            meta_next = True
    else:
        # just another token, append to the line
        line.append(tuple(d.split("\t")))

sorted_syntax = sorted(cards_by_syntax.items(), key=lambda s:len(s[1]), reverse=True)
for s in sorted_syntax:
    print("\t".join([str(len(s[1])), str(len(s[0])), " ".join(s[0]), " ".join(s[1])]))
