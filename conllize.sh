#!/bin/bash

TESTING=false
PARSER_EVAL=bazel-bin/syntaxnet/parser_eval
MODEL_DIR=syntaxnet/models/parsey_mcparseface
INPUT_FORMAT=stdin

fake_process() {
    echo "v-- I WOULD PROCESS THIS PART --v"
    echo -e "$1"
    echo "^-------------------------------^"
}

parsey() {
    $PARSER_EVAL \
      --input=$INPUT_FORMAT \
      --output=stdout-conll \
      --hidden_layer_sizes=64 \
      --arg_prefix=brain_tagger \
      --graph_builder=structured \
      --task_context=$MODEL_DIR/context.pbtxt \
      --model_path=$MODEL_DIR/tagger-params \
      --slim_model \
      --batch_size=1024 \
      --alsologtostderr \
       | \
      $PARSER_EVAL \
      --input=stdin-conll \
      --output=stdout-conll \
      --hidden_layer_sizes=512,512 \
      --arg_prefix=brain_parser \
      --graph_builder=structured \
      --task_context=$MODEL_DIR/context.pbtxt \
      --model_path=$MODEL_DIR/parser-params \
      --slim_model \
      --batch_size=1024 \
      --alsologtostderr
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
                echo "$card" | parsey
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
