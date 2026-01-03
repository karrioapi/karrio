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
// REGISTERINTDOC from Server
echo "<h2>registerIntDoc-Function</h2><hr>";

$params = array(
  "InternationalDoc" => array(
  		array(
  		     			'InternationalDoc' => array(
			                'ConsignerCustomsID' => "123456",
			                'Invoice' => 1,
			                'InvoiceNo' => "12345",
			                'Certificate' => 1,
			                'CertificateNo' => "12345",
			                'PrintInternationalDocuments' => 1,
			                'InternationalDocumentFormat' => array(
			                		'Type' => "PDF",
			                		'Size' => "CN22"
			                ),
			                'ShipToRef' => "",
			                'TotalWeightkg' => "34.000",
			                'Postage' => "2.45",
			                'ItemCategory' => 5,
			                'ContentsDesc' => array(
			                  	array(
			                		'Contents' => "Books and Brochures",
			                		'ItemValue' => "12.05",
			                		'NetWeight' => "3.065",
			                		'Origin' => "DE",
			                		'Quantity' => 5,
			                		'TariffNumber' => "12345678"
			                		),
			                  	array(
			                		'Contents' => "Books",
			                		'ItemValue' => "12.04",
			                		'NetWeight' => "3.063",
			                		'Origin' => "AU",
			                		'Quantity' => 4,
			                		'TariffNumber' => "12345679"
			                		)
			                )
 					),
     			'IDShipment' => array(
			                'ShipmentRefField' => "TrackingID",
			                'ShipmentRefValue' => "9998800006463"
 					),
     			'IDPackage' => array(
			                'PackageRefField' => "",
			                'PackageRefValue' => ""
 					)

    		)
    	)
);

echo "<h3>var_dump of Result: </h3>";
try
{
	$result = $client->registerIntDoc($params);
	var_dump($result);

	$documentdata = $result->registerIntDocResult->printDocumentsResult->Document;
	$decodeddata = base64_decode($documentdata);
	echo "<br><br><a href='data:application/pdf;base64,".$documentdata."' target = 'Doc1'>Document 1</a>";

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
