<?php 
$options = array(
    'soap_version' => SOAP_1_1,
    'exceptions' => true,
    'trace' => 1,
    'cache_wsdl' => WSDL_CACHE_NONE,
    'compression' => SOAP_COMPRESSION_ACCEPT | SOAP_COMPRESSION_GZIP,
    'location' => 'https://sandboxapi.awiwe.solutions/version4/shippingwcfsandbox/ShippingWCF.svc/Shippingwcf',
    'connection_timeout' => 300
);
$client = new SoapClient($url, $options);
$client->__setSoapHeaders(Array(new WsseAuthHeader($username, $password),new WsseApiKeyHeader($apikey),new WsseCultureHeader($culture)));
?>