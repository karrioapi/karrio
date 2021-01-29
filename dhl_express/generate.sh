SCHEMAS=$1
find ./pydhl -name "*.py" -exec rm -r {} \;
touch ./pydhl/__init__.py

generateDS --no-namespace-defs -o "./pydhl/dct_response_global_2_0.py" $SCHEMAS/DCT-Response_global-2.0.xsd
generateDS --no-namespace-defs -o "./pydhl/dct_req_global_2_0.py" $SCHEMAS/DCT-req_global-2.0.xsd
generateDS --no-namespace-defs -o "./pydhl/dct_requestdatatypes_global.py" $SCHEMAS/DCTRequestdatatypes_global.xsd
generateDS --no-namespace-defs -o "./pydhl/dct_responsedatatypes_global.py" $SCHEMAS/DCTResponsedatatypes_global.xsd
generateDS --no-namespace-defs -o "./pydhl/tracking_request_known_1_0.py" $SCHEMAS/TrackingRequestKnown-1.0.xsd
generateDS --no-namespace-defs -o "./pydhl/tracking_request_unknown_1_0.py" $SCHEMAS/TrackingRequestUnknown-1.0.xsd
generateDS --no-namespace-defs -o "./pydhl/tracking_response.py" $SCHEMAS/TrackingResponse.xsd
generateDS --no-namespace-defs -o "./pydhl/book_pickup_global_req_3_0.py" $SCHEMAS/book-pickup-global-req-3.0.xsd
generateDS --no-namespace-defs -o "./pydhl/book_pickup_global_res_3_0.py" $SCHEMAS/book-pickup-global-res-3.0.xsd
generateDS --no-namespace-defs -o "./pydhl/cancel_pickup_global_req_3_0.py" $SCHEMAS/cancel-pickup-global-req-3.0.xsd
generateDS --no-namespace-defs -o "./pydhl/cancel_pickup_global_res.py" $SCHEMAS/cancel-pickup-global-res.xsd
generateDS --no-namespace-defs -o "./pydhl/datatypes_global_v62.py" $SCHEMAS/datatypes_global_v62.xsd
generateDS --no-namespace-defs -o "./pydhl/err_res.py" $SCHEMAS/err-res.xsd
generateDS --no-namespace-defs -o "./pydhl/modify_pickup_global_req_3_0.py" $SCHEMAS/modify-pickup-global-req-3.0.xsd
generateDS --no-namespace-defs -o "./pydhl/modify_pickup_global_res_3_0.py" $SCHEMAS/modify-pickup-global-res-3.0.xsd
generateDS --no-namespace-defs -o "./pydhl/pickup_err_res.py" $SCHEMAS/pickup-err-res.xsd
generateDS --no-namespace-defs -o "./pydhl/pickup_res.py" $SCHEMAS/pickup-res.xsd
generateDS --no-namespace-defs -o "./pydhl/pickupdatatypes_global_3_0.py" $SCHEMAS/pickupdatatypes_global-3.0.xsd
generateDS --no-namespace-defs -o "./pydhl/routing_err_res.py" $SCHEMAS/routing-err-res.xsd
generateDS --no-namespace-defs -o "./pydhl/routing_global_req_2_0.py" $SCHEMAS/routing-global-req-2.0.xsd
generateDS --no-namespace-defs -o "./pydhl/routing_global_res.py" $SCHEMAS/routing-global-res.xsd
generateDS --no-namespace-defs -o "./pydhl/ship_val_err_res.py" $SCHEMAS/ship-val-err-res.xsd
generateDS --no-namespace-defs -o "./pydhl/ship_val_global_req_6_2.py" $SCHEMAS/ship-val-global-req-6.2.xsd
generateDS --no-namespace-defs -o "./pydhl/ship_val_global_res_6_2.py" $SCHEMAS/ship-val-global-res-6.2.xsd
generateDS --no-namespace-defs -o "./pydhl/track_err_res.py" $SCHEMAS/track-err-res.xsd