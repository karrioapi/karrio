<?php 
require_once('UserSettings.php');
require_once('WsseAuthHeader_Class.php');
require_once('WsseApiKeyHeader_Class.php');
require_once('WsseCultureHeader_Class.php');
require_once('InitSoapClient_ShippingWCF.php');
//****************************************************************************************************************************
echo "<h1>Implementation Sample for ShippingWCF (SANDBOX) in PHP</h1><hr>";
echo "<h2>getProfiles, getCEPs, getProducts & getServices with Countries-Check</h2>";
//****************************************************************************************************************************
// GETPROFILES from Server
echo "<hr><h2>getProfiles-Function with Countries-Check - 2 level (only Mandators and CEPs)</h2><hr>";
echo "<h3>var_dump of Result: </h3>";

$params = array(
  "level" => 2,
  "Countries" => array('DK','AT')	
);

var_dump($client->GetProfiles($params));

/*echo "<br><br>REQUEST:\n" . $client->__getLastRequest() . "\n";
echo "<br><br>REQUESTHEADERS:\n" . $client->__getLastRequestHeaders() . "\n";
echo "<br><br>RESPONSE:\n" . $client->__getLastResponse() . "\n";
echo "<br><br>RESPONSEHEADERS:\n" . $client->__getLastResponseHeaders() . "\n";*/

//****************************************************************************************************************************

// GETCEPs vs Countries from Server
echo "<hr><h2><br><strong>getCEPs-Function with Countries-Check - 1 level</strong><hr>";
$params = array(
  "Mandator" => "1",
  "level" => 1,
  "Countries" => array('DK','AT')	
);

echo "<h3>var_dump of Result: </h3>";
var_dump($client->GetCEPs($params) );

/*echo "<br><br>REQUEST:\n" . $client->__getLastRequest() . "\n";
echo "<br><br>REQUESTHEADERS:\n" . $client->__getLastRequestHeaders() . "\n";
echo "<br><br>RESPONSE:\n" . $client->__getLastResponse() . "\n";
echo "<br><br>RESPONSEHEADERS:\n" . $client->__getLastResponseHeaders() . "\n";*/

//****************************************************************************************************************************

// GETProducts from Server - ONLY 1 LEVEL
echo "<hr><h2>getProducts-Function with Countries-Check - 1 Level</h2><hr>";
$params = array(
  "Mandator" => "1",
  "CEP" => "UPS",
  "level" => 1,
  "Countries" => array('DK','AT')	
);

echo "<h3>var_dump of Result: </h3>";
var_dump($client->GetProducts($params) );

/*echo "<br><br>REQUEST:\n" . $client->__getLastRequest() . "\n";
echo "<br><br>REQUESTHEADERS:\n" . $client->__getLastRequestHeaders() . "\n";
echo "<br><br>RESPONSE:\n" . $client->__getLastResponse() . "\n";
echo "<br><br>RESPONSEHEADERS:\n" . $client->__getLastResponseHeaders() . "\n";*/

//****************************************************************************************************************************
// GETProducts from Server - ALL LEVELS
echo "<hr><h2>getProducts-Function with Countries-Check - all levels</h2><hr>";
$params = array(
  "Mandator" => "1",
  "CEP" => "UPS",
  "level" => 0,
  "Countries" => array('DK','AT')	
);

echo "<h3>var_dump of Result: </h3>";
var_dump($client->GetProducts($params) );

/*echo "<br><br>REQUEST:\n" . $client->__getLastRequest() . "\n";
echo "<br><br>REQUESTHEADERS:\n" . $client->__getLastRequestHeaders() . "\n";
echo "<br><br>RESPONSE:\n" . $client->__getLastResponse() . "\n";
echo "<br><br>RESPONSEHEADERS:\n" . $client->__getLastResponseHeaders() . "\n";*/

//****************************************************************************************************************************

// GETServices from Server
echo "<hr><h2>getServices-Function with Countries-Check</h2><hr>";
$params = array(
  "Mandator" => "1",
  "CEP" => "UPS",
  "Product" => "11",
  "Countries" => array('DK','AT')	
);

echo "<h3>var_dump of Result: </h3>";
 var_dump($client->GetServices($params) );

/*echo "<br><br>REQUEST:\n" . $client->__getLastRequest() . "\n";
echo "<br><br>REQUESTHEADERS:\n" . $client->__getLastRequestHeaders() . "\n";
echo "<br><br>RESPONSE:\n" . $client->__getLastResponse() . "\n";
echo "<br><br>RESPONSEHEADERS:\n" . $client->__getLastResponseHeaders() . "\n";*/
 //****************************************************************************************************************************
echo "<hr><h2>END of Sample functions</h2>";
echo "J&ouml;rk Sternsdorff, Awiwe Solutions GmbH";
?>