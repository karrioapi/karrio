SCHEMAS=$1
find ./pycanadapost -name "*.py" -exec rm -r {} \;
touch ./pycanadapost/__init__.py

generateDS --no-namespace-defs -o "./pycanadapost/authreturn.py" $SCHEMAS/authreturn.xsd
generateDS --no-namespace-defs -o "./pycanadapost/common.py" $SCHEMAS/common.xsd
generateDS --no-namespace-defs -o "./pycanadapost/customerinfo.py" $SCHEMAS/customerinfo.xsd
generateDS --no-namespace-defs -o "./pycanadapost/discovery.py" $SCHEMAS/discovery.xsd
generateDS --no-namespace-defs -o "./pycanadapost/manifest.py" $SCHEMAS/manifest.xsd
generateDS --no-namespace-defs -o "./pycanadapost/merchantregistration.py" $SCHEMAS/merchantregistration.xsd
generateDS --no-namespace-defs -o "./pycanadapost/messages.py" $SCHEMAS/messages.xsd
generateDS --no-namespace-defs -o "./pycanadapost/ncshipment.py" $SCHEMAS/ncshipment.xsd
generateDS --no-namespace-defs -o "./pycanadapost/openreturn.py" $SCHEMAS/openreturn.xsd
generateDS --no-namespace-defs -o "./pycanadapost/pickup.py" $SCHEMAS/pickup.xsd
generateDS --no-namespace-defs -o "./pycanadapost/pickuprequest.py" $SCHEMAS/pickuprequest.xsd
generateDS --no-namespace-defs -o "./pycanadapost/postoffice.py" $SCHEMAS/postoffice.xsd
generateDS --no-namespace-defs -o "./pycanadapost/rating.py" $SCHEMAS/rating.xsd
generateDS --no-namespace-defs -o "./pycanadapost/serviceinfo.py" $SCHEMAS/serviceinfo.xsd
generateDS --no-namespace-defs -o "./pycanadapost/shipment.py" $SCHEMAS/shipment.xsd
generateDS --no-namespace-defs -o "./pycanadapost/track.py" $SCHEMAS/track.xsd
