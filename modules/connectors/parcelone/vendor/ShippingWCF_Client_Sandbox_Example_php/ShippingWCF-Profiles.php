<?php 
require_once('UserSettings.php');
require_once('WsseAuthHeader_Class.php');
require_once('WsseApiKeyHeader_Class.php');
require_once('WsseCultureHeader_Class.php');
require_once('InitSoapClient_ShippingWCF.php');
//****************************************************************************************************************************
echo "<h1>Implementation Sample for ShippingWCF (SANDBOX) in PHP</h1><hr>";
echo "<h2>getProfiles, getCEPs, getProducts & getServices without Countries-Check</h2>";
echo "<hr><h2>getProfiles-Funktion</h2><hr>";

echo "<strong>var_dump of Result: </strong><br>";
var_dump($client->GetProfiles());

/*echo "<br><br>REQUEST:\n" . $client->__getLastRequest() . "\n";
echo "<br><br>REQUESTHEADERS:\n" . $client->__getLastRequestHeaders() . "\n";
echo "<br><br>RESPONSE:\n" . $client->__getLastResponse() . "\n";
echo "<br><br>RESPONSEHEADERS:\n" . $client->__getLastResponseHeaders() . "\n";*/

//****************************************************************************************************************************

// GETCEPs from Server
echo "<hr><h2>getCEPs-Function - all level</h2><hr>";
$params = array(
  "Mandator" => "1"
);

echo "<strong>var_dump of Result: </strong><br>";
var_dump($client->GetCEPs($params) );

/*echo "<br><br>REQUEST:\n" . $client->__getLastRequest() . "\n";
echo "<br><br>REQUESTHEADERS:\n" . $client->__getLastRequestHeaders() . "\n";
echo "<br><br>RESPONSE:\n" . $client->__getLastResponse() . "\n";
echo "<br><br>RESPONSEHEADERS:\n" . $client->__getLastResponseHeaders() . "\n";*/
//****************************************************************************************************************************

// GETProducts from Server - ONLY 1 LEVEL
echo "<hr><h2>getProducts-Function - 1 level</h2><hr>";
$params = array(
  "Mandator" => "1",
  "CEP" => "UPS",
  "level" => 1
);

echo "<strong>var_dump of Result: </strong><br>";
var_dump($client->getProducts($params) );

/*echo "<br><br>REQUEST:\n" . $client->__getLastRequest() . "\n";
echo "<br><br>REQUESTHEADERS:\n" . $client->__getLastRequestHeaders() . "\n";
echo "<br><br>RESPONSE:\n" . $client->__getLastResponse() . "\n";
echo "<br><br>RESPONSEHEADERS:\n" . $client->__getLastResponseHeaders() . "\n";*/

//****************************************************************************************************************************
// GETProducts from Server - ALL LEVELS
echo "<hr><h2>getProducts-Function - All Levels</h2><hr>";
$params = array(
  "Mandator" => "1",
  "CEP" => "UPS"
);

echo "<strong>var_dump of Result: </strong><br>";
var_dump($client->getProducts($params) );

/*echo "<br><br>REQUEST:\n" . $client->__getLastRequest() . "\n";
echo "<br><br>REQUESTHEADERS:\n" . $client->__getLastRequestHeaders() . "\n";
echo "<br><br>RESPONSE:\n" . $client->__getLastResponse() . "\n";
echo "<br><br>RESPONSEHEADERS:\n" . $client->__getLastResponseHeaders() . "\n";*/

//****************************************************************************************************************************

// GETServices from Server
echo "<hr><h2>getServices-Function</h2><hr>";
$params = array(
  "Mandator" => "1",
  "CEP" => "UPS",
  "Product" => "11"
);

echo "<strong>var_dump of Result: </strong><br>";
 var_dump($client->getServices($params) );

/*echo "<br><br>REQUEST:\n" . $client->__getLastRequest() . "\n";
echo "<br><br>REQUESTHEADERS:\n" . $client->__getLastRequestHeaders() . "\n";
echo "<br><br>RESPONSE:\n" . $client->__getLastResponse() . "\n";
echo "<br><br>RESPONSEHEADERS:\n" . $client->__getLastResponseHeaders() . "\n";*/
 
//****************************************************************************************************************************
echo "<hr><h2>END of Sample functions</h2>";
echo "J&ouml;rk Sternsdorff, Awiwe Solutions GmbH";
?>