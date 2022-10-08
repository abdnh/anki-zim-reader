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
if [ "$spacy" = true ]; then
    pip install spacy==3.4.1 -t src/vendor
    python -m spacy download el_core_news_sm -t src/vendor
fi

# Web assets
npm install
mkdir -p src/web/vendor
cp node_modules/tippy.js/dist/tippy.umd.min.js src/web/vendor/
cp node_modules/tippy.js/dist/tippy.umd.min.js src/web/vendor/
cp node_modules/tippy.js/dist/tippy.css src/web/vendor/
cp node_modules/tippy.js/themes/light.css src/web/vendor/
cp node_modules/tippy.js/animations/scale-extreme.css src/web/vendor/
cp node_modules/@popperjs/core/dist/umd/popper.min.js src/web/vendor/
