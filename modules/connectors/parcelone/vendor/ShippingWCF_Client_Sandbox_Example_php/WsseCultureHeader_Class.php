<?php
class WsseCultureHeader extends SoapHeader {
	function __construct($culture) {
	    	    parent::__construct('culture','culture',$culture,false);
	}
}
?>
