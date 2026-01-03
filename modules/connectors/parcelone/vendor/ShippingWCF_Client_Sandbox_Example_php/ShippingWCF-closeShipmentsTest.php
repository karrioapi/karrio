<?php
// Display of Documents only works with Firefox or Chrome, not with IE.
require_once('UserSettings.php');
require_once('WsseAuthHeader_Class.php');
require_once('WsseApiKeyHeader_Class.php');
require_once('WsseCultureHeader_Class.php');
require_once('InitSoapClient_ShippingWCF.php');
//****************************************************************************************************************************
echo "<h1>Implementation Sample for ShippingWCF (SANDBOX) in PHP</h1><hr>";
//****************************************************************************************************************************
echo "<h2>closeShipments</h2><hr>";

$params = array(
	'ClosedStamp' => "",
	'Mandator' => "",
	'Consigner' => "",
	'CEP' => "PA1",
	'Format' => array(
				'Type' => "PDF"
				),
	'Shipments'  => array(
    	)
);

echo "<h3>var_dump of Result: </h3>";
try
{
	$result = $client->closeShipments($params);
	var_dump($result);

	$documentdata = $result->closeShipmentsResult->ClosedResult->printDocumentResult->Document;
	$decodeddata = base64_decode($documentdata);

	echo "<br><br><a href='data:application/pdf;base64,".$documentdata."' target = 'ClosingReport1'>Closing Report</a>";
}
catch (SoapFault  $fault)
{
	echo $fault ->faultcode;
	echo ": ";
	echo $fault->faultstring;

}

echo "<br><br>REQUEST:\n" . $client->__getLastRequest() . "\n";
echo "<br><br>REQUESTHEADERS:\n" . $client->__getLastRequestHeaders() . "\n";
echo "<br><br>RESPONSE:\n" . htmlentities($client->__getLastResponse()) . "\n";
echo "<br><br>RESPONSEHEADERS:\n" . $client->__getLastResponseHeaders() . "\n";

//****************************************************************************************************************************
echo "<hr><h2>END of Sample function</h2>";
echo "J&ouml;rk Sternsdorff, Awiwe Solutions GmbH";
?>
