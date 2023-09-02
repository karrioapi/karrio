SCHEMAS=./schemas
LIB_MODULES=./colissimo_lib
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

generateDS --no-namespace-defs -o "${LIB_MODULES}/services.py" "${SCHEMAS}/services.xsd"
