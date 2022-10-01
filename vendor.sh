pip install git+https://github.com/abdnh/zimply-core@eddf548b778d9046020ba84d9912257d1cb949fb -t src/vendor
# TODO: make spacy optional
pip install spacy==3.4.1 -t src/vendor
python -m spacy download el_core_news_sm -t src/vendor
# TODO: download tippy.js
