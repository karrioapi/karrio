<?php 
// Display of Documents only works with Firefox or Chrome, not with IE.
require_once('UserSettings.php');
require_once('WsseAuthHeader_Class.php');
require_once('WsseApiKeyHeader_Class.php');
require_once('WsseCultureHeader_Class.php');
require_once('InitSoapClient_ShippingWCF.php');
//****************************************************************************************************************************
echo "<h1>Implementation Sample for ShippingWCF (SANDBOX) in PHP</h1><hr>";
echo "<h2>PRINTDOCUMENTS-Function</h2><hr>";

$params = array(
	  "PrintRequests" => array(
	  		array(
	     			'DocType' => "HighValueReport",
	     			'Format' => array('Type' => "PDF"),
	     			'IDShipment' => array(
	     					'ShipmentRefField' => "ShipmentID",
	     					'ShipmentRefValue' => "9998800000973")
	     			)
	    		)
	);
try {
	$result = $client->printDocuments($params);
	//  var_dump($result);
	$documentdata = $result->printDocumentsResult->printDocumentsResult[0]->Document;
	$decodeddata = base64_decode($documentdata);
	$documentdata2 = $result->printDocumentsResult->printDocumentsResult[1]->Document;
	$decodeddata2 = base64_decode($documentdata2);
	
	echo "<br><br><a href='data:application/pdf;base64,".$documentdata."' target = 'Doc1'>Document 1</a>";
	echo "<br><br><a href='data:application/pdf;base64,".$documentdata2."' target = 'Doc2'>Document 2</a>";
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
