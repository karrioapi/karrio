SCHEMAS=./schemas
LIB_MODULES=./andreani_lib
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

