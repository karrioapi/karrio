SCHEMAS=./schemas
find ./pycanpar -name "*.py" -exec rm -r {} \;
touch ./pycanpar/__init__.py

generateDS --no-namespace-defs -o "./pycanpar/CanparAddonsService.py" $SCHEMAS/CanparAddonsService.xsd
generateDS --no-namespace-defs -o "./pycanpar/CanparRatingService.py" $SCHEMAS/CanparRatingService.xsd
generateDS --no-namespace-defs -o "./pycanpar/CanshipBusinessService.py" $SCHEMAS/CanshipBusinessService.xsd