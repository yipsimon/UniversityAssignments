<?php

require_once('MDB2.php'); 

$host='co-project.lboro.ac.uk'; 
$dbName='group09';

$username='group09'; 
$password='rnt65gem';    			
$dsn = "mysql://$username:$password@$host/$dbName";


$db = & MDB2::connect($dsn);        # make connection, & Assign By Reference 

if (PEAR::isError($db)) { 			# alert for errors or use global error handler 
	die($db->getMessage());    
}

$db->setFetchMode(MDB2_FETCHMODE_ASSOC);	

$sql = $_REQUEST["sql"];		#Request the sql statement

$res =& $db->query($sql);

if (PEAR::isError($res)) {
    die($res->getMessage());
}

$Allresult = Array();

while ($result = $res->fetchRow()) {
	$result['image'] = base64_encode($result['image']);		#For each result, we will convert the image data into base64 place it back into the array
	array_push($Allresult, $result);

}

echo json_encode($Allresult);	#echo as json

?>