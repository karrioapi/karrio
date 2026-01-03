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
     			'Software' => "WCF Test",
     			'ShipmentRef' => "123456",
     			'DocumentFormat' => array('Type' => "PDF"),
     			'LabelFormat' =>  array('Type' => "GIF"),
     			'ReturnShipmentIndicator' => 0,
     			'PrintLabel' => 1,
     			'ShipToData' => array(
     				'Name1' => UTF8_Encode("Jörk Sternsdorff"),
     				'Name2' => "z.Hd. Martin Sternsdorff",
     				'Name3' => "",
 					'PrivateAddressIndicator' => 1,
 					'ShipmentAddress' => array(
			                'City' => "Sao Paolo",
			                'PostalCode' => "268A3",
			                'Street' => UTF8_Encode("rue Vanessa 6"),
			                'Streetno' => "",
			                'Country' => "BR"
 					)
     			),
     			'Packages' => array(
     				array(
						'PackageWeight' => array('Value' => "2.200"),
						'PackageID' => "1",
            'IntDocData' => array(
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
                )
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
