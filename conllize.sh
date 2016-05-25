#!/bin/bash

TESTING=false

fake_process() {
    echo "v-- I WOULD PROCESS THIS PART --v"
    echo -e "$1"
    echo "^-------------------------------^"
}

cd ~/models/syntaxnet

card=""
initial_comments=true
while read line; do
    if echo "$line" | grep -q "^<"; then
        # translate pointy bracket metadata to conll comment
        comment=$(echo "$line" | cut -d '>' -f 1)
        remainder=$(echo "$line" | cut -d '>' -f 2-)
        echo "#$comment>"
        if [ -n "$remainder" ]; then
            card=$(echo "$card"; echo "$remainder")
        fi
    elif [ -z "$line" ]; then
        if $initial_comments; then
            # we only just finished the headers and don't have a card yet
            initial_comments=false
        else
            # our card is finished, pass it on
            if $TESTING; then
                fake_process "$card"
            else
                echo "$card" | syntaxnet/demo.sh 2>/dev/null
            fi
            card=""
        fi
        echo
    else
        # multi-line card, keep appending
        if [ -z "$card" ]; then
            card="$line"
        else
            card=$(echo "$card"; echo "$line")
        fi
    fi
done

cd - 2>/dev/null
