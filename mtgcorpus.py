#!/usr/bin/python3

import json
import sys
import argparse
import re

# Parse command-line options.
parser = argparse.ArgumentParser(description="Translate a JSON Magic set file to plaintext.")
parser.add_argument("-q", "--quiet", action="store_true", help="squelch unnecessary metadata (ability words and reminder text)")
args = parser.parse_args()

# Parse JSON from stdin.
edition = json.loads(sys.stdin.read())

# Start with headers giving some information about the set.
print("""<Set: {}>
<Block: {}>
<Release Date: {}>
<Border: {}>""".format(edition["name"], edition.get("block", "n/a"), edition["releaseDate"], edition["border"]))

for card in edition["cards"]:
    # Only include cards that have any rules text.
    if "text" in card:
        # The concordancers I'm using are bad at Unicode, let's go easy on them.
        # (These characters come up on subtypes and modal spells.)
        types = card["type"].replace("—", "-")
        rules = card["text"].replace("—", "-").replace("•", "*")

        # We find more interesting collocates if we abstract out card names.
        rules = rules.replace(card["name"], "~")
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
            rules = re.sub("<[^>]*>", "", rules)

        print()
        # Add more metadata: name, cost, types, rarity.
        print("<{}>".format(card["name"]))
        print("<{} / {} / {}>".format(card.get("manaCost", ""), types, card["rarity"]))

        # The only concordancer-visible content is the actual rules.
        print(rules)
