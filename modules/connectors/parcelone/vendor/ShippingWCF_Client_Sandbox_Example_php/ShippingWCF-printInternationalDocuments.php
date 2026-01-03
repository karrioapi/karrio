<?php 
require_once('UserSettings.php');
require_once('WsseAuthHeader_Class.php');
require_once('WsseApiKeyHeader_Class.php');
require_once('WsseCultureHeader_Class.php');
require_once('InitSoapClient_ShippingWCF.php');
//****************************************************************************************************************************
$params = array(
	  "PrintRequests" => array(
	  		array(
	     			'DocType' => "CN23",
	     			'Format' => array('Type' => "PDF"),
	     			'IDShipment' => array(
	     					'ShipmentRefField' => "TrackingID",
	     					'ShipmentRefValue' => "1Z79Y03F6894669944"),
	     			'IDPackage' => null
	     					
	     			)
	    		)
	);
try {
	$result = $client->printInternationalDocuments($params);
	//var_dump($result);
	$documentdata = $result->printInternationalDocumentsResult->printDocumentsResult->Document;
	$decodeddata = base64_decode($documentdata);
	
	header("Content-type: application/pdf"); 
	header('Content-disposition: inline; filename=test.pdf');
	//header("Content-Disposition: attachment; filename=downloaded.pdf");
	header("Content-length: ". strlen($decodeddata)); 
	echo ($decodeddata);
}
catch (SoapFault  $fault)
{
	echo $fault ->faultcode;
	echo ": ";
	echo $fault->faultstring;
}	
?>
