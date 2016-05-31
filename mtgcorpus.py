#!/usr/bin/python3

import json
import sys
import argparse
import re

# Parse command-line options.
parser = argparse.ArgumentParser(description="Translate a JSON Magic set file to plaintext.")
parser.add_argument("-q", "--quiet", action="store_true", help="squelch most non-rules text (headers, ability words, and reminder text)")
parser.add_argument("-s", "--split", action="store_true", help="split abilities into one line per sentence")
parser.add_argument("-n", "--name", action="store_true", help="use NAME instead of ~ to replace a card's name in its rules text")
parser.add_argument("-r", "--rulings", action="store_true", help="output rulings text instead of card text")
args = parser.parse_args()

# Parse JSON from stdin.
edition = json.loads(sys.stdin.read())

# Start with headers giving some information about the set.
if not args.quiet:
    print("""<Set: {}>
    <Block: {}>
    <Release Date: {}>
    <Border: {}>""".format(edition["name"], edition.get("block", "n/a"), edition["releaseDate"], edition["border"]))

for card in edition["cards"]:
    # Only include cards that have any rules text.
    if not "text" in card:
        continue

    if args.rulings:
        if not "rulings" in card:
            continue
        rules = "\n".join([c["text"] for c in card["rulings"]])
    else:
        rules = card["text"]

    # The concordancers I'm using are bad at Unicode, let's go easy on them.
    # (These characters come up on subtypes and modal spells.)
    types = card["type"].replace("—", "-")
    rules = rules.replace("—", "-").replace("•", "*")

    # We find more interesting collocates if we abstract out card names.
    if args.name:
        replacement = "NAME"
    else:
        replacement = "~"
    rules = rules.replace(card["name"], replacement)

    if not args.rulings:
        # Hide reminder text by putting it in angle brackets.
        rules = rules.replace("(", "<(").replace(")", ")>")
        # Split the rules into lines to find ability words and hide them too.
        lines = rules.splitlines()
        for i, line in enumerate(lines):
            if " - " in line and not line.startswith("Choose"):
                lines[i] = "<" + line.replace("- ", "-> ")
        rules = "\n".join(lines)

    if args.quiet:
        # Strip all the stuff we just identified.
        rules = re.sub(" ?<[^>]*> ?", "", rules)

    if args.split:
        # Split multi-sentence abilities into one sentence per line.
        # The predictability of Magic rules text writing allows us
        # to do this VERY naively. (May miss some rulings.)
        rules = rules.replace(". ", ".\n")

    print()
    # Add more metadata: name, cost, types, rarity.
    print("<{}>".format(card["name"]))
    print("<{} / {} / {}>".format(card.get("manaCost", ""), types, card["rarity"]))

    # The only concordancer-visible content is the actual rules.
    print(rules)
