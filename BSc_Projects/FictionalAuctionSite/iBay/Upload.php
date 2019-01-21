<?php
session_start();
if (!isset( $_SESSION['username'])){
	$loggedIn = 0;
}
else{
	$userId = $_SESSION['username'];
	$loggedIn = 1;
}
// determines whether a user is logged in so they can be redirected if not

if(isset($_REQUEST['Logout'])){
		session_unset();
		session_destroy(); 
}
//	ends the session when the user logs out

if(isset($_REQUEST['UserProfile'])){
		header('Location: UserProfile.php');
}
// gets the user's profile data if they are logged in

require_once('MDB2.php'); 

$con = mysqli_connect("co-project.lboro.ac.uk", "group09", "rnt65gem", "group09");
$host='co-project.lboro.ac.uk'; 
$dbName='group09';

$username='group09'; 
$password='rnt65gem';    			

$dsn = "mysql://$username:$password@$host/$dbName";

// API package supports portable SQL statements 

$db = & MDB2::connect($dsn);        // make connection & assign by reference 

if (PEAR::isError($db)) { 			
	die($db->getMessage());    
}
// displays the error message if one occurs
	
$db->setFetchMode(MDB2_FETCHMODE_ASSOC);
// sets the type of array that retrieved data will be stored in

$itemData = Array();

if (isset($_REQUEST['itemId'])){
	$sqltype = 1;
	$itemNo = $_REQUEST['itemId'];
	$sql = "SELECT * FROM `iBayItems` LEFT JOIN iBayImages ON iBayItems.itemId = iBayImages.itemId WHERE iBayItems.itemId = ".$itemNo." ";

	$res =& $db->query($sql);
	if (PEAR::isError($res)) { 			
	die($res->getMessage());    
	}
	$resArray = Array();
	while ($result = $res->fetchRow()) {
		$result['image'] = base64_encode($result['image']);
		array_push($resArray, $result);
		}
		
		$itemData = json_encode($resArray);
}	// prepares the item data (retrieved from database) if an item is being edited
	// and sets the page to 'update' version

else{
	$itemNo = '';
	$sqltype = 0;
}	// sets the page to 'upload' version


	$imageOK = 1;
	

if(isset($_REQUEST['submit_item'])){
	$title = $_REQUEST['item_name'];
	$category = $_REQUEST['category'];
	$description = $_REQUEST['description'];
	$price = $_REQUEST['initial_price'];
	$postage = $_REQUEST['postage'];
	$start = $_REQUEST['start_time'];
	$finish = $_REQUEST['end_time'];
	$itemNo2 = $_REQUEST['itemId2'];
	$sqltype = $_REQUEST['sqltype2'];
	// extracts the form field data once the 'submit' button is pressed
	
	$primary_name = mysql_escape_string(file_get_contents($_FILES['primary_img_upload']["tmp_name"]));
	$primary_size = round($_FILES['primary_img_upload']["size"]/1024);
	$primary_mime = $_FILES['primary_img_upload']["type"];
	// extracts the main image and separates the data into the required fields for the database
	
	$prim_MimeCheck = getimagesize($_FILES['primary_img_upload']["tmp_name"]);
    if($prim_MimeCheck == false) {
        $imageOK = 0;
    } // checks to make sure the primary image file is a real image
	
	$otherimg = $_FILES['other_img_upload']["name"];
	
	foreach($otherimg as $key => $img){
		$other_MimeCheck = getimagesize($_FILES['primary_img_upload']["tmp_name"]);
		if($other_MimeCheck == false) {
			$imageOK = 0;
		} 
	} // similarly, checks the images in the array

	if ($imageOK == 1){ // the code is executed if the images are valid
	
		if ($sqltype == 0){	// runs the following code if the user is uploading an item
	
			$sql_itemId = mysqli_query($con, "SELECT MAX(itemId) As Id FROM iBayItems");
			$row_it = mysqli_fetch_assoc($sql_itemId);
			$itemId = $row_it['Id'] + 1;
			// prepares the item ID value for the image insert query
	
			$sql_item = "INSERT INTO `iBayItems`( `userId`, `title`, `category`,`description`,
				`price`, `postage`, `start`, `finish`)
				VALUES ( '".$userId."', '".$title."', '".$category."', '".$description."', '".$price."',
					'".$postage."', '".$start."', '".$finish."')";
			// query to insert the item into the database using the extracted data
			
			$res =	mysqli_query($con, $sql_item);  // runs the query using the established connection
			
			$sql_imgId = mysqli_query($con, "SELECT MAX(imageId) As ID FROM iBayImages");
			$row_im = mysqli_fetch_assoc($sql_imgId);
	
			$imgId = $row_im['ID']; // sets up the image ID for the image insert query
	
			$sql_prim = "INSERT INTO `iBayImages` (`imageId`, `image`, `mimeType`, `imageSize`, `itemId`, `Mainimage`) 
				VALUES (' ', '".$primary_name."', '".$primary_mime."', '".$primary_size."', '".$itemId."', '1')";
			// query to insert the main image into the database
	
			$res = mysqli_query($con, $sql_prim);	// runs the query
		
			$imgId = $imgId + 1;	// increments the image ID value
		
			foreach($otherimg as $key => $img){
		
				$other_name = mysql_escape_string(file_get_contents($_FILES['other_img_upload']["tmp_name"][$key]));
				$other_size = round($_FILES['other_img_upload']["size"][$key]/1024);
				$other_mime = $_FILES['other_img_upload']["type"][$key];
		
				$sql_other = "INSERT INTO `iBayImages` (`image`, `mimeType`, `imageSize`, `itemId`, `Mainimage`) 
					VALUES ('".$other_name."', '".$other_mime."', '".$other_size."', '".$itemId."', '0')";
				
				$res = mysqli_query($con, $sql_other);
		
				$imgId = $imgId + 1;	
			}	// loop preparing and inserting each image after the main image
		}	
		else if ($sqltype == 1){	// the following code is executed if the user is editing an item
			
			if(isset($itemNo2)){
				$updateNo = $itemNo2;
			}
			else{
				$updateNo = $itemNo;
			}
			// gets the ID number of the item for later use
	
			$itemId = $updateNo;
	
			$del_images = "DELETE FROM iBayImages WHERE itemID = '".$updateNo."'";
			// deletes all images for the item being edited (this is to prevent multiple main images)
		
			$res = mysqli_query($con, $del_images);
	
			$sql_imgId = mysqli_query($con, "SELECT MAX(imageId) As ID FROM iBayImages");
			$row_im = mysqli_fetch_assoc($sql_imgId);
	
			$imgId = $row_im['ID'];
			// prepares the image ID for the new images to be inserted
	
			$sql_prim = "INSERT INTO `iBayImages` (`imageId`, `image`, `mimeType`, `imageSize`, `itemId`, `Mainimage`) 
				VALUES (' ', '".$primary_name."', '".$primary_mime."', '".$primary_size."', '".$updateNo."', '1')";
	
			$res = mysqli_query($con, $sql_prim);
			// inserts the new main image into the database
	
			$imgId = $imgId + 1;	// increments the image ID
			
			foreach($otherimg as $key => $img){
		
				$other_name = mysql_escape_string(file_get_contents($_FILES['other_img_upload']["tmp_name"][$key]));
				$other_size = round($_FILES['other_img_upload']["size"][$key]/1024);
				$other_mime = $_FILES['other_img_upload']["type"][$key];
	
				$sql_other = "INSERT INTO `iBayImages` (`image`, `mimeType`, `imageSize`, `itemId`, `Mainimage`) 
					VALUES ('".$other_name."', '".$other_mime."', '".$other_size."', '".$updateNo."', '0')";
		
				$res = mysqli_query($con, $sql_other);
		
				$imgId = $imgId + 1;	
			}	// loop preparing and inserting the images into the database
			
			$sql_edit = "UPDATE iBayItems SET title = '".$title."', category  = '".$category."',
						description = '".$description."', price = '".$price."', postage = '".$postage."',
						start = '".$start."', finish = '".$finish."' WHERE itemId = ".$updateNo." ";
			// query for updating the item using the new data

			$res = mysqli_query($con, $sql_edit);
			
			header('Location: UserProfile.php');
			// redirects the user to their profile page after executing the queries
		}
	}
	else if ($imageOK == 0){
		echo "File is not a valid image.";
		break;
	}	// if any images are not valid, returns a message but does not execute any queries
}
	
?>


<html>
<head>

<meta charset="UTF-8">

<title>Seller's Upload Page</title>
<link type="text/css" rel="stylesheet" href="stylemain.css">	<!-- CSS file is linked here -->

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script>
<!-- jQuery API linked here -->

<script type="text/javascript">

$(document).ready(function(){	// jQuery is run upon document load completion
	var user = <?php echo $loggedIn; ?>;
	if (user == 0){
		alert("Please log in to upload an item");
		window.location = "Login.php";
	}	// login validation: redirects to the login page if no user is logged in
	else if (user == 1){
		var type = <?php echo $sqltype; ?>;
		
		if (type == 1){
			var initialdata = <?php echo $itemData; ?>;
			
			$("#title").val(initialdata[0].title);
			$("#price").val(initialdata[0].price);
			$("#minbid").val(initialdata[0].price);
			$("#start").val(initialdata[0].start);
			$("#finish").val(initialdata[0].finish);
			$("#desc").val(initialdata[0].description);
			$("#postage").val(initialdata[0].postage);
			$("#cat").val(initialdata[0].category);
			
		}
	}	// if a valid user is editing an item, script autocompletes form fields using data from the database
});

</script>
<style>
#desc{
	font-family:"Verdana", sans-serif;
	color:#20878E;
	border-color:#20878E;
	border:3px solid #20878E;
	border-radius:5px;
	font-size:12px;
	margin-left:15px
}
#cat{
	font-family:"Verdana", sans-serif;
	color:#20878E;
	border-color:#20878E;
	border:3px solid #20878E;
	border-radius:5px;
	font-size:12px;
	margin-left:15px	
}
input[type='file']{
	color:#51B0B8;
	font-family:"Verdana",sans-serif;
	padding: 5px 15px; 
	border:0 none;
	cursor:pointer;
}
#uploadtable{
	margin-left:100px;
	margin-top:10px;
}
#submit_item{
	position:absolute;
	font-size:12px;
	padding:10px;
	border-radius: 25px;
}

</style>
</head>
<body>
<div id="header">
	
	<?php 
	if(isset($_SESSION['username']) && $_SESSION['username']!= "user" ){
	?>
		<div id="loggedon">
		<form action="iBay-main.php" method="get">
		<input type="submit" class="user_logged" name="UserProfile" value="Your Account">
		<input type="submit" class="user_logged" name="Logout" value="Log Out">
		</form>
		</div> 		<!-- a logged in user can access their profile or log out -->
	<?php }
	else{?>
	<div> <a href="Login.php" id="signin_reg">Login or Register</a>	</div>	<!-- otherwise, the login page is linked -->
	<?php } ?>
		<a id="logo_pos" href="iBay-main.php">
			<img src="logo.png" width="200">
		</a>
		<div id="nav">
		<form name="defaultsearch" action="SearchResults.php" method="get">
		<ul id="navbar">
			<li><input type="submit" class="navElement" name="search_default" value="Fashion" /></li>
			<li><input type="submit" class="navElement" name="search_default" value="Sports" /></li>
			<li><input type="submit" class="navElement" name="search_default" value="Books" /></li>
			<li><input type="submit" class="navElement" name="search_default" value="Gaming" /></li>
			<li><input type="submit" class="navElement" name="search_default" value="Electronics" /></li>
		</ul>
		</form>
		</div>
		<form name="mainsearch" action="SearchResults.php" method="get">
			<input type="text" id="searchbar" name="search_input" placeholder="What are you looking for..." size="70"/>
			<input type="submit" id="searchbutton" value="Search it..." />
		</form>
		<a id="adv" href="AdvancedSearch.php">Advanced Search</a>
	</div>	<!-- logo and navigation options are displayed at the top of the page -->
<div class="main">
<table id="uploadtable" ><tr><td>
	<h1>Upload a new item</h1>
	<form name="item" id="item" action="Upload.php" method="post" enctype="multipart/form-data">	<!-- form for uploading items is generated -->
	<label class="uploadlabel" for="Name_item">Name of item:</label><input type="text" id="title" name="item_name" size="50" required><br><br>			
	<!-- title (text) field is created -->
	
	<label class="uploadlabel" for="Price">Price:</label><input type="number" id="price" name="initial_price" min="0" step="0.01" required><br><br>
	<!-- initial price (non-negative 2 decimal place float) field is created -->
					
	<label class="uploadlabel" for="StartTime">Start time:</label><input type="datetime-local" id="start" name="start_time" placeholder="YYYY-MM-DD HH:MM:SS" size=30 required>(YYYY-MM-DD HH:MM:SS)<br><br>
	<label class="uploadlabel" for="FinishTime">Finish time:</label><input type="datetime-local" id="finish" name="end_time" placeholder="YYYY-MM-DD HH:MM:SS" size=30 required>(YYYY-MM-DD HH:MM:SS)<br><br>
	<!-- start and finish timestamp fields are created, with the required format specified to the user -->
	
	<label class="uploadlabel" for="Category">Category:</label><select id="cat" name="category">	<!-- category drop-down box created -->
		<option value="fashion">Fashion</option>
		<option value="sports">Sports</option>
		<option value="books">Books</option>
		<option value="games">Gaming</option>
		<option value="electronics">Electronics</option>
		</select><br><br>
		
	<label class="uploadlabel" for="Postage">Postage:</label><input class="uploadlabel" type="number" id="postage" name="postage" min="0" step="0.01" required>
	<br><br>
	<!-- postage (non-negative 2 decimal place float) field is created -->
		
	<label class="uploadlabel" for="Description">Description:</label><textarea id="desc" name="description" rows="10" cols="90" maxlength="1000" required></textarea>
	<br>
	<!-- description (textarea) field created -->
		
		
	<label class="uploadlabel" for="Primimg">Primary image:</label><input type="file" name="primary_img_upload" id="primary_img_upload" value="Browse" accept="image/*" required /><br>
	If you are editing an item, please re-upload the primary image (existing images are removed)
	<br><br>
	<label class="uploadlabel" for="Otherimg">Other images:</label><input type="file" name="other_img_upload[]" id="other_img_upload" value="Browse" accept="image/*" multiple required /><br>
	If you are editing an item, please re-upload any images you wish to keep
	<br><br>
	<!-- main and secondary image (file) fields created -->
		
	<input type="hidden" id="itemId2" name="itemId2" value="<?php echo $itemNo; ?>"/>
	<!-- hidden field for storing the item ID value when page refreshes -->
	
	<input type="hidden" id="sqltype2" name="sqltype2" value="<?php echo $sqltype; ?>"/>
	<!-- hidden field for determining which version of the page to load upon refresh -->
	
	<input type="submit" id="submit_item" name="submit_item" value="Save changes"><br><br>
	<!-- button to submit the form -->
		
	</form> 
	
	
	
	
	</td></tr></table>
</div>




</body>
</html>