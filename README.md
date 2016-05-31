# mtgcorpus
(c) 2016 Finn Ellis. I will figure out a license at some point. If you actually want this for something before I do that, email me! finnre@pdx.edu

This repository contains a set of scripts for connecting the output of [mtgjson.com](http://mtgjson.com) to the input of [Parsey McParseface](https://github.com/tensorflow/models/tree/master/syntaxnet)--which is to say, for turning JSON representations of Magic: the Gathering card data into corpus files tagged by part of speech in [CONLL format](http://universaldependencies.org/format.html).


## example
Here's a piece of the original JSON from the Shadows Over Innistrad set file dump:

```
{
    "layout": "double-faced",
    "name": "Archangel Avacyn",
    "power": "4",
    "artist": "James Ryman",
    "multiverseid": 409741,
    "supertypes": [
        "Legendary"
    ],
    "cmc": 5,
    "number": "5a",
    "rarity": "Mythic Rare",
    "colors": [
        "White"
    ],
    "imageName": "archangel avacyn",
    "names": [
        "Archangel Avacyn",
        "Avacyn, the Purifier"
    ],
    "text": "Flash\nFlying, vigilance\nWhen Archangel Avacyn enters the battlefield, creatures you control gain indestructible until end of turn.\nWhen a non-Angel creature you control dies, transform Archangel Avacyn at the beginning of the next upkeep.",
    "types": [
        "Creature"
    ],
    "subtypes": [
        "Angel"
    ],
    "manaCost": "{3}{W}{W}",
    "type": "Legendary Creature \u2014 Angel",
    "id": "02ea5ddc89d7847abc77a0fbcbf2bc74e6456559",
    "colorIdentity": [
        "W",
        "R"
    ],
    "toughness": "4"
}
```

Here's the analogous portion of the output of `mtgcorpus.py`, a human-readable but untagged representation of some of the same information. Metadata (everything that isn't rules text, including reminder text and ability words) is in pointy brackets.

```
<Archangel Avacyn>
<{3}{W}{W} / Legendary Creature - Angel / Mythic Rare>
Flash
Flying, vigilance
When ~ enters the battlefield, creatures you control gain indestructible until end of turn.
When a non-Angel creature you control dies, transform ~ at the beginning of the next upkeep.
```

`mtgcorpus.py` takes a few optional arguments which clean the data up for use in later parts of the pipeline:

```
usage: mtgcorpus.py [-h] [-q] [-s] [-n]

Translate a JSON Magic set file to plaintext.

optional arguments:
  -h, --help   show this help message and exit
  -q, --quiet  squelch non-rules text (headers, ability words, and reminder
               text)
  -s, --split  split abilities into one line per sentence
  -n, --name   use NAME instead of ~ to replace a card's name in its rules
               text
```

Here's the output of `conllize.sh` for that same block. Metadata is now in # comments (and also pointy brackets). 

```
#<Archangel Avacyn>
#<{3}{W}{W} / Legendary Creature - Angel / Mythic Rare>
1       Flash   _       NOUN    NNP     _       0       ROOT    _       _

1       Flying  _       NOUN    NN      _       0       ROOT    _       _
2       ,       _       .       ,       _       1       punct   _       _
3       vigilance       _       NOUN    NN      _       1       dep     _       _

1       When    _       ADV     WRB     _       3       advmod  _       _
2       ~       _       .       NFP     _       3       mark    _       _
3       enters  _       VERB    VBZ     _       7       advcl   _       _
4       the     _       DET     DT      _       5       det     _       _
5       battlefield     _       NOUN    NN      _       3       dobj    _       _
6       ,       _       .       ,       _       7       punct   _       _
7       creatures       _       VERB    VBZ     _       0       ROOT    _       _
8       you     _       PRON    PRP     _       9       nsubj   _       _
9       control _       VERB    VBP     _       7       ccomp   _       _
10      gain    _       NOUN    NN      _       9       ccomp   _       _
11      indestructible  _       ADJ     JJ      _       10      dobj    _       _
12      until   _       ADP     IN      _       10      prep    _       _
13      end     _       NOUN    NN      _       12      pobj    _       _
14      of      _       ADP     IN      _       13      prep    _       _
15      turn    _       NOUN    NN      _       14      pobj    _       _
16      .       _       .       .       _       7       punct   _       _

1       When    _       ADV     WRB     _       7       advmod  _       _
2       a       _       DET     DT      _       4       det     _       _
3       non-Angel       _       ADJ     JJ      _       4       amod    _       _
4       creature        _       NOUN    NN      _       7       nsubj   _       _
5       you     _       PRON    PRP     _       6       nsubj   _       _
6       control _       VERB    VBP     _       4       rcmod   _       _
7       dies    _       VERB    VBZ     _       9       advcl   _       _
8       ,       _       .       ,       _       9       punct   _       _
9       transform       _       VERB    VB      _       0       ROOT    _       _
10      ~       _       VERB    VBN     _       9       dobj    _       _
11      at      _       ADP     IN      _       9       prep    _       _
12      the     _       DET     DT      _       13      det     _       _
13      beginning       _       NOUN    NN      _       11      pobj    _       _
14      of      _       ADP     IN      _       13      prep    _       _
15      the     _       DET     DT      _       17      det     _       _
16      next    _       ADJ     JJ      _       17      amod    _       _
17      upkeep  _       NOUN    NN      _       14      pobj    _       _
18      .       _       .       .       _       9       punct   _       _
```

Finally, `summarize.py` takes an entire CONLLized set file and groups card names by the syntax of sentences in their rules. When doing this, you'll want to have used the -s (split into sentences) and probably -q (squelch non-rules text) options to `mtgcorpus.py` (see above).

A card as complex as Archangel Avacyn will appear many places in the summary output, but here's one example. This is the line that on Avacyn contains "Flying, vigilance" but on Felidar Sovereign is "Vigilance, lifelink," on Ghostly Sentinel is "Flying, vigilance," and so on.

```
15      NN , NN <Felidar Sovereign> <Ghostly Sentinel> <Akoum Firebird> <Woodland Wanderer> <Misthoof Kirin> <Shieldhide Dragon> <Dragonlord Dromoka> <Dragonlord Kolaghan> <Steppe Glider> <Tajuru Pathwarden> <Stormchaser Mage> <Eagle of the Watch> <Archangel Avacyn> <Goldnight Castigator> <Werewolf of Ancient Hunger>
```

# usage

1. Follow the [instructions for setting up SyntaxNet](https://github.com/tensorflow/models/tree/master/syntaxnet). Clone it into your home directory, or else edit `conllize.sh` to reflect where you actually put it.
2. Get the set files of your choice from [mtgjson.com](http://mtgjson.com/). We want the individual set files specifically because they include set-specific metadata. Unzip as needed.
3. You should now have a bunch of JSON files in a directory, named things like `RTR.json`. Run `maketxt.sh` to automatically convert them into text files named things like `RTR.txt`, or convert individual files with `cat SOM.json | ./mtgcorpus.py -qns > SOM.txt`. (The mass-conversion script will add the -qns flags automatically.)
4. Likewise, you can `makeconll.sh` to convert text files to CONLL files en masse, or simply `cat BNG.txt | ./conllize.sh > BNG.conll`. This part takes a while! Be patient.
5. You can summarize the rules by syntax the same way: `cat FRF.conll | ./summarize.py > FRF_by_syntax.txt`. If you used -q to omit the headers, you can cat together a bunch of CONLL files and summarize them all together: `cat *.conll | ./summarize.py > summary.txt`.

The entire processing pipeline for a single set, on one line:

`cat MMA.json | ./mtgcorpus.py -qns | ./conllize.sh | ./summarize.py > MMA_by_syntax.txt`

The entire processing pipeline for a bunch of sets, on one line:

`./maketxt.sh && ./makeconll.sh && cat *.conll | ./summarize.py > summary.txt`
