<?php 
// Display of Documents only works with Firefox or Chrome, not with IE.
require_once('UserSettings.php');
require_once('WsseAuthHeader_Class.php');
require_once('WsseApiKeyHeader_Class.php');
require_once('WsseCultureHeader_Class.php');
require_once('InitSoapClient_ShippingWCF.php');
//****************************************************************************************************************************
echo "<h1>Implementation Sample for ShippingWCF (SANDBOX) in PHP</h1><hr>";
echo "<h2>getClosedStamps-Function</h2><hr>";

try {
	$result = $client->getClosedStamps(array('Mandator' => "",'Consigner' => "",'CEP' => "",	'StartDate' => "20160316000000",'EndDate' => "20160316120000"));
	var_dump($result);
}
catch (SoapFault  $fault)
{
	echo $fault ->faultcode;
	echo ": ";
	echo $fault->faultstring;
}	
echo "<hr>";

echo "<br><br>REQUEST:\n" . htmlentities($client->__getLastRequest()) . "\n";
echo "<br><br>REQUESTHEADERS:\n" . $client->__getLastRequestHeaders() . "\n";
echo "<br><br>RESPONSE:\n" . htmlentities($client->__getLastResponse()) . "\n";
echo "<br><br>RESPONSEHEADERS:\n" . $client->__getLastResponseHeaders() . "\n";

//****************************************************************************************************************************
echo "<hr><h2>END of Sample function</h2>";
echo "J&ouml;rk Sternsdorff, Awiwe Solutions GmbH";
?>
