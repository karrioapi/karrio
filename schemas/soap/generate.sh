SCHEMAS=$1
find ./soap_lib/ -name "*.py" -exec rm -r {} \;
echo "from soap_lib.envelope import Header, Body, Envelope" > ./soap_lib/__init__.py

generateDS --no-namespace-defs -o "./soap_lib/envelope.py" ./schemas/schemas.xmlsoap.org.xml
