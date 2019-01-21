<?php

require_once('MDB2.php'); 

$host='co-project.lboro.ac.uk'; 
$dbName='group09';

$username='group09'; 
$password='rnt65gem';    			# For security, authentication use an include file on co-project

$dsn = "mysql://$username:$password@$host/$dbName";

      	# API package supports portable SQL statements 

$db = & MDB2::connect($dsn);        # make connection, & Assign By Reference 

if (PEAR::isError($db)) { 			# alert for errors or use global error handler 
	die($db->getMessage());    
}

$db->setFetchMode(MDB2_FETCHMODE_ASSOC);	


?>