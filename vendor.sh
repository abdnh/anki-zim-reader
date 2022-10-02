spacy=false
while getopts ":s" option; do
   case $option in
      s)
         spacy=true
         ;;
   esac
done
pip install -U git+https://github.com/abdnh/zimply-core@f682cedd8c774da2c492203e2ab75f6b7228a92c -t src/vendor
if [ "$spacy" = true ]; then
    pip install spacy==3.4.1 -t src/vendor
    python -m spacy download el_core_news_sm -t src/vendor
fi

# TODO: download tippy.js
