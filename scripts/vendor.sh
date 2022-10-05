#!/bin/bash

spacy=false
while getopts ":s" option; do
   case $option in
      s)
         spacy=true
         ;;
   esac
done
pip install -U --no-deps git+https://github.com/abdnh/zimply-core@09c6f0f004591e0642590210248e87ff72bb6e21 -t src/vendor
./scripts/setup_pyzstd.sh
if [ "$spacy" = true ]; then
    pip install spacy==3.4.1 -t src/vendor
    python -m spacy download el_core_news_sm -t src/vendor
fi
./scripts/setup_tippyjs.sh
