<?php
class WsseApiKeyHeader extends SoapHeader {
	function __construct($apikey) {
	    	    parent::__construct('apikey','apikey',$apikey,false);
	}
}
?>
