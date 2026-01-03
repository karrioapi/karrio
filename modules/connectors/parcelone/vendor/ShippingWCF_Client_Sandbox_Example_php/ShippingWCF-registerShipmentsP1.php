<?php
require_once('UserSettings.php');
require_once('WsseAuthHeader_Class.php');
require_once('WsseApiKeyHeader_Class.php');
require_once('WsseCultureHeader_Class.php');
require_once('InitSoapClient_ShippingWCF.php');
//****************************************************************************************************************************
echo "<h1>Implementation Sample for ShippingWCF (SANDBOX) in PHP</h1><hr>";
//****************************************************************************************************************************
// REGISTERSHIPMENTS from Server
echo "<h2>registerShipments-Function</h2><hr>";

$params = array(
  "ShippingData" => array(
  		array(
     			'MandatorID' => "1",
     			'ConsignerID' => "1",
     			'CEPID' => "PA1",
     			'ProductID' => "eco",  // possible: ecoL, basicL, plusL, eco, basic, plus
     			'Software' => "WCF Sandbox",
     			'ShipmentRef' => "123456",
     			'DocumentFormat' => array('Type' => "PDF"),
     			'LabelFormat' =>  array('Type' => "GIF"),
     			'ReturnShipmentIndicator' => 0,
     			'PrintLabel' => 1,
     			'ShipToData' => array(
     				'Name1' => UTF8_Encode("Jörk Sternsdorff"),
     				'Name2' => "z.Hd. Elena Sternsdorff",
     				'Name3' => "",
 					'PrivateAddressIndicator' => 1,
 					'ShipmentAddress' => array(
			                'City' => "Wien",
			                'PostalCode' => "1001",
			                'Street' => UTF8_Encode("RambaZamba-Str. 6"),
			                'Streetno' => "",
			                'Country' => "AT"
 					)
     			),
     			'Packages' => array(
     				array(
						'PackageWeight' => array('Value' => "2.200"),
						'PackageID' => "1"
					)
     			)
    		)
    	)
);

echo "<h3>var_dump of Result: </h3>";
try
{
	$result = $client->registerShipments($params);
	var_dump($result);
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
