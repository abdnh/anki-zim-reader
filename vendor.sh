spacy=false
while getopts ":s" option; do
   case $option in
      s)
         spacy=true
         ;;
   esac
done

pip install git+https://github.com/abdnh/zimply-core@eddf548b778d9046020ba84d9912257d1cb949fb -t src/vendor
if [ "$spacy" = true ]; then
    pip install spacy==3.4.1 -t src/vendor
    python -m spacy download el_core_news_sm -t src/vendor
fi

# TODO: download tippy.js
