find . -name "*.pyc" | xargs rm -rf
find . -name "__pycache__" | xargs rm -rf
rm -r -f conf/vocabularies
