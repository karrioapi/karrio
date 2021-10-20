SCHEMAS=$1
find ./pysoap/ -name "*.py" -exec rm -r {} \;
echo "from pysoap.envelope import Header, Body, Envelope" > ./pysoap/__init__.py

generateDS --no-namespace-defs -o "./pysoap/envelope.py" ./schemas/schemas.xmlsoap.org.xml
