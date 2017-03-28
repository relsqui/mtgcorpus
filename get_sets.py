#!/usr/bin/python3

import os
import json
from urllib import request

url = "http://mtgjson.com/json/{0}.json"

if not os.path.exists("sets"):
    os.makedirs("sets")

# Get the list of available sets from the AllSets file.
with request.urlopen(url.format("AllSets")) as f:
    sets = json.loads(f.read().decode()).keys()

# Get the individual file for each set.
for s in sets:
    with request.urlopen(url.format(s + "-x")) as f:
        data = f.read().decode()
    filename = s + ".json"
    with open(os.path.join("sets", filename), "w") as f:
        print("Writing", filename)
        f.write(data)
