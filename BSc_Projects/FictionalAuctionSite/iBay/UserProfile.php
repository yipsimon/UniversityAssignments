<?php
	include "dbconnect.php";
	session_start();
	
	//has the user pressed the 'Logout' button, then destory their session
	if(isset($_REQUEST['Logout'])){
		session_unset();
		session_destroy(); 
		//echo "All session variables are now removed, and the session is destroyed.";
	}
	//has the user pressed the 'Your Account' button. If so, link them there
	if(isset($_REQUEST['UserProfile'])){
		header('Location: UserProfile.php');
	}
	
	//get the username of the session
	$username = $_SESSION['username'];
	
	//SQL query to get all member information
	$sql = "SELECT * FROM iBayMembers WHERE userId = '".$username."';";
	
	//query it using the database connection db
	$res =& $db->query($sql);
	//if an error is returned from the database, kill the query and return the error message
	if (PEAR::isError($res)) {
		die($res->getMessage());
	}
	
	//get all results of the query (should just be 1)
	$resu = $res->fetchAll();
	
	
	//SQL query to get the items and information that the current user is selling
	$sql = "SELECT items.itemId, items.title,items.price,items.postage,items.userId,items.finish,items.highestBidder,images.image FROM iBayItems AS items INNER JOIN iBayImages AS images ON items.itemId=images.itemId AND
				items.userId='".$username."' AND images.Mainimage='1' ORDER BY items.finish ASC Limit 5"; 
	
	//SQL query to get the items and information that the user is currently the highestBidder on
	$sql1 ="SELECT items.itemId, items.title,items.price,items.postage,items.userId,items.finish,images.image FROM iBayItems AS items INNER JOIN iBayImages AS images ON items.itemId=images.itemId AND 
				items.highestBidder='".$username."' AND images.Mainimage='1' ORDER BY items.finish ASC Limit 5";
		
	//query selling SQL	
	$sth = $db->query($sql);
	
	//declare an array to store all the items and info being sold 
	$sell = array();
	
	//put all the requested info from the SQL command into the array
	while ($row = $sth->fetchRow()) {
			$row['image'] = base64_encode($row['image']);
			array_push($sell, $row);
	}
	
	//encode the array such that we can use the array and it's data within client side 
	$sell = json_encode($sell);
	
	
	//query the highestBidder SQL
	$sth = $db->query($sql1);
	//stores the buying/bought information returned
	$buy = array();
	//put the information returned in the array
	while ($row = $sth->fetchRow()) {
			$row['image'] = base64_encode($row['image']);
			array_push($buy, $row);
	}

	//encode the array so we can use it client side
	$buy = json_encode($buy);
	
	//if the user has selected to delete an item
	if (isset($_REQUEST['deleteId'])) {
		//get the itemId of the item they wannt to delete
		$deleteId = $_REQUEST['deleteId'];
		//SQL command to delete the selected item
		$deleteSql = "DELETE iBayItems , iBayImages FROM iBayItems INNER JOIN iBayImages WHERE iBayItems.itemId=iBayImages.itemId and iBayItems.itemId = '".$deleteId."'";
			
		//query it	
		$res1 =& $db->query($deleteSql);
	
		//if an error occurs, kill the request to the database and ouput the returned error message
		if (PEAR::isError($res1)) {
  	  		die($res1->getMessage());
		}
		//tell the user that the updates were made
 		echo "<script> alert('Updates made.'); </script>";
		//return them to the UserProfile page
		header('Location: UserProfile.php');
		
	}
	
	//if the user has pressed the update button
	if (isset ($_REQUEST['Update'])) { 
		if ($_REQUEST['passwordn']!= "" ) {
			
			//SQL query to update the information including a new password
			$sql95= "UPDATE iBayMembers SET password='".$_REQUEST["passwordn"]."', name='".$_REQUEST["name"]."', email='".$_REQUEST["email"]."', address='".$_REQUEST["address"]."', postcode='".$_REQUEST["postcode"]."' WHERE userId='".$username."'";
			//query it
 			$res95 =& $db->query($sql95);
			//if an error, return the error message
 			if (PEAR::isError($res95)) {
  	  			die($res95->getMessage());
			}
		}
		else {
			//SQL query to update the information excluding a new password
			$sql22= "UPDATE iBayMembers SET name='".$_REQUEST["name"]."', email='".$_REQUEST["email"]."', address='".$_REQUEST["address"]."', postcode='".$_REQUEST["postcode"]."' WHERE userId='".$username."'";
 			$res22 =& $db->query($sql22);
			if (PEAR::isError($res22)) {
  	  			die($res22->getMessage());
			}
		}
		//return to the user profile page
		header('Location: UserProfile.php');
	}
	
	//encode all seller information so we can use it server side
	$result = json_encode($resu);
	
?>
<html>
    <head>
        <title>User Profile</title>
		<link type="text/css" rel="stylesheet" href="stylemain.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
		<script type='text/javascript'>

			var sell = <?php echo $sell; ?>;        //array to store the encoded selling items
			var buy = <?php echo $buy; ?>;          //array to store the encoded buying items
			var selllength = Object.keys(sell).length;    //get the number of items being sold
			var buylength = Object.keys(buy).length;      //get the number of items being/has been bought
			//these are all variables used for displaying images, ie)we want to display 4 images
			var startsell = 0;                        
			var endsell = 4;
			var startbuy = 0;
			var endbuy = 4;
			var userinfo = <?php echo $result;?>;    //array to store encoded seller information
			var pw = userinfo[0].password;           //get user's password
		
			//on page load
			$(document).ready(function(){
				
				//the following is used to create a long string of HTML code which will display all the users information.
				var html = '<p id="userdetails"><label class="userlabel" for="Name"><b>Name: </b>'+userinfo[0].name+'</label>';
					html += '<label class="emaillabel" for="Email"><b>Email: </b>'+userinfo[0].email+'</label><br>';
					html += '<label class="userlabel" for="Address"><b>Address: </b>'+userinfo[0].address+'</label>';
					html += '<label class="userlabel" for="Postcode"><b>Postcode: </b>'+userinfo[0].postcode+'</label>';
					html += '<label class="userlabel" for="Rating"><b>Rating: </b>'+userinfo[0].rating+'</label></p><br>';
					
					html += '<form id="personalInfo" action="UserProfile.php" method="get" style= "display: none" onsubmit="return checkdetails()" ><table id="tableinfo" ><tr><td>';
					html += '<label class="loginlabel" for="Name">Name:</label><input name="name" id="name" size="30" value="'+userinfo[0].name+'" required>';
					html += '<br><label class="loginlabel" for="Email">Email:</label><input type="email" style="width:250px" name="email" id="email" size="16" value="'+userinfo[0].email+'" required><br>';
					html += '<label class="loginlabel" for="Address">Address:</label><textarea name="address" id="address" rows="4" cols="40" maxlength="100" required>'+userinfo[0].address+'</textarea><br>';
					//<input type="textarea" name="address" id="address" rows="10" cols="50" maxlength="50" value="'+userinfo[0].address+'">';
					html += '<label class="loginlabel" for="Postcode">Postcode:</label><input name="postcode" id="postcode" size="16" value="'+userinfo[0].postcode+'" required><br>';
					html += '</td><td><h4>Change Password</h4><label class="uploadlabel" for="OldPassword">Current Password:</label><input type="Password" name="password" id="password" size="16" required><br>';
					html += '<label class="uploadlabel" for="NewPassword">New Password:</label><input type="Password" name="passwordn" id="passwordn" size="16"><br>';
					html += '<label class="" for="RPassword">Repeat New Password:</label><input type="Password" name="passwordv" id="passwordv" size="16"><br>';
					html += '<span class="errmsg" id="invalidpass"></span><br><br><br>';
		    		html += '<input type="submit" style="float:right;" name="Update" id="Update" value="Update Information" ></td></tr></table></form>';
				
				//we then append all this HTML code to the area with id='userinfo' using JQuery
				$("#userinfo").append(html);
				
				//if there are no selling items
				if(selllength == 0 ){
					//set the table to be empty except for a message to say there are no items
					$('#sellitemsItems').html("");
					var items1 =  "<table class='contenttable'><tr>";
						items1 = "<td>No Items Uploaded</td><br></tr></table>"
					//append it to the id='sellitemsItems' section.
					$('#sellitemsItems').html(items1);
				}
				//otherwise if there are items to sell
				else{
					//if there are less than 4 items being sold
					if(endsell >= selllength){
						//then we only display the number being sold
						endsell = selllength;
					}
					//create a table to display all the selling items
					createtable(sell,startsell,endsell,'sellitemsItems');
				}
				//if there are no items being bought
				if(buylength == 0){
					//set table to empty apart from a message which says no items are being bought
					$('#biditemsItems').html("");
					var items1 =  "<table class='contenttable'><tr>";
						items1 = "<td>No leading items Bidded</td><br></tr></table>"
					$('#biditemsItems').html(items1);
				}
				else{
					//if number of buy items is >=4
					if(endbuy >= buylength){
						//only display 4
						endbuy = buylength;
					}
					//create the table of buy items
					createtable(buy,startbuy,endbuy,'biditemsItems');
				}
												
			});
			
			// this is run when the 'update information' button is clicked by the user
			
			 function checkdetails(){
				var cp = $('#password').val();
				var np = $('#passwordn').val();
				var npv = $('#passwordv').val();
				// this if statement checks if the current password supplied does not match the one found in the database, if the do then the updates will be made.
				if( cp != pw ){	
					alert("Invalid password");
					return false;
				}
				// this if statement checks if the new password does not match the password verification. If it does, then the update will be made to include the new password. 
				if( np != npv){
					alert("Please re-enter your new password.");
					return false;
				}
				// this clarifies to the user that the wanted updates to personal information have been made.
				alert("Updates made.");
			}
			
			//create a table which will store information and images
			function createtable(data,x,y,title){
					//takes in the data to display, a start and final data and the title of the id of the area to put the table
					var items1 =  "<table class='contenttable'><tr>";
					//clear the area with the id that has been passed
					$('#'+title).html("");
					
					//create a string of HTML code to display all the information in a table
					for (var i = x; i < y; i++){  
						items1 += "<td class='itemdisplay'><img class='imagelinkitem' src='data:image/jpeg;base64,"+data[i].image+"' onclick=itemlink("+data[i].itemid+") />";
						items1 += "<br><button class='titlelinkitem' onclick=itemlink("+data[i].itemid+") >"+data[i].title+"</button>";
						items1 += "<ul class='noliststy' ><li><label class='itemlabel2' for='Price'>Price :</label>"+"£"+data[i].price+'</li>';
						items1 += "<li><label class='itemlabel2' for='Postage'>Postage Cost :</label>"+data[i].postage+'</li>';
						items1 += "<li><label class='itemlabel2' for='Seller'>SellerID :</label>"+data[i].userid+'</li>';
						items1 += "<li><label class='itemlabel2' for='TRemain'>Finish Date :</label><br>"+data[i].finish+'</li>';
						
						var un = data[i].finish;
						var time = un.replace(" ", "T"); 
						var deadline = getTimeRemaining(time);
						//if we are creating table for selling items and the time remaining is <0
						if(title == 'sellitemsItems' && parseInt(deadline.total) < 0 ){
								//if there is a highest bidder of the item
								if( data[i].highestBidder != null){
									//The item is sold and give the highest bidder username
									items1 += "<li><br><label class='soldlabel' for='Sold'>Sold to User:</label><br>"+data[i].highestBidder+'<br></li>';
								}
								//if there isn't a highest bidder, say the item is not sold and add a button to delete the item
								else{
									
									items1 += "<li><br><label class='soldlabel' for='UnSold'>Not Sold</label><br></li>";
								    items1 += "<button type='submit' class='edititem' name='deleteButton' onClick='deleteSellItem("+data[i].itemid+")'>Delete</button></li>";
								}
						}
					
						//if the item is being sold by user and has time remaining
						if (title == 'sellitemsItems' && parseInt(deadline.total) >= 0){
							//add edit buttons and delete buttons
							items1 += "<br><li style='margin-left:-30px;' ><button type='submit' class='edititem' name='editButton' onClick='editItem("+data[i].itemid+")'>Edit</button>";
							items1 += "<button type='submit' class='edititem' name='deleteButton' onClick='deleteSellItem("+data[i].itemid+")'>Delete</button></li>";
						}
						
						//if the item is being bought
						if (title == 'biditemsItems'){
							//if the item has finished 
							if(parseInt(deadline.total) < 0){
								//add some text to say the user has won it
								items1 += "<li><br><label class='soldlabel' for='Won'>Won</label><br></li>";
							}
							else{
								//otherwise say it is ongoing
								items1 += "<li><br><label class='soldlabel' for='ongoing'>On Going</label><br></li>";
							}	
						}
						
						
						items1 += "<br></ul></td>";
					}
					
					if( y < 3 && x == 0 ){
						var z = y-4;
						for ( var i = 0; i < z; i++){
							items1 +="<td class='emptyitem'><br></td>";
							alert(i);
						}
					}
					
					items1 += "</tr></table>";
					//set the area with the id passed equal to the HTML string created
					$('#'+title).html(items1);
			}
			
			//function to calculate the remaining time of the item auction in miliseconds
			function getTimeRemaining(endtime) {
				var t = Date.parse(endtime) - Date.parse(new Date());
				var seconds = Math.floor((t / 1000) % 60);
				var minutes = Math.floor((t / 1000 / 60) % 60);
				var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
				var days = Math.floor(t / (1000 * 60 * 60 * 24));
				return {
					'total': t,
					'days': days,
					'hours': hours,
					'minutes': minutes,
					'seconds': seconds
				};
			}
			
			//change the images
			function changeimage(type,direction) {
					//if we are chaning the sell items
					if( type == "sell"){
					var tempstart = startsell + direction;
					var tempend = endsell + direction;
						//if there are no more images alert to this
						if(direction == 1 && tempend > selllength){
							alert("end of page");
						}
						else if(direction == -1 && tempstart < 0){
							alert("Reached the top of page");
						}
						//otherwise update the table of images
						else{
							startsell = tempstart;
							endsell = tempend;
							createtable(sell,startsell,endsell,"sellitemsItems");
						}
				}
				//if we are changing the buy images
				if( type == "buy"){
					var tempstart = startbuy + direction;
					var tempend = endbuy + direction;
						//if there are no more images aler to this
						if(direction == 1 && tempend > buylength){
							alert("end of page");
						}
						else if(direction == -1 && tempstart < 0){
							alert("Reached the top of page");
						}
						//otherwise update the table of images
						else{
							startbuy = tempstart;
							endbuy = tempend;
							createtable(buy,startbuy,endbuy,"biditemsItems");
					}
				}	
			}	
			
		// this toggles the two tables created from show to hide. This function is enacted when the user clicks 'edit'. 		
		function changeEdit(){
			$("#userdetails").toggle();
			$("#personalInfo").toggle();
		}
		
		function deleteSellItem(sellItemID){
			$('#deleteId').val(sellItemID);
			document.getElementById("hiddenDeleteItem").submit();
		}
		
		function editItem(Item){
			$('#itemId').val(Item);
			document.getElementById("hiddenEditItem").submit();
		}
		function itemlink(x){
				$("#itemid").val(x);
				document.getElementById("itemresult").submit();
			}
		
		
		</script>
		<style>
		.noliststy{
			list-style-type: none;
		}
		.contenttable{
			border: none;
			border-collapse: collapse;
			width: 1060px;
		}
		.contenttable td{
			border: none;
			border-collapse: collapse;
			color: #51B0B8;
			font-family:"Verdana",sans-serif;
			padding:10px;
			font-size:12px;
		}
		td.liveitem{
			border:5px solid red;
			padding:2px;
		}
		
		td.itemdisplay{
			width:260px;
		}
		
		#tableinfo{
			border: none;
			border-collapse: collapse;
		}
		#tableinfo td{
			float:left;
		}
		.userlabel{
			font-size:16px;
			width:250px;
			height:25px;
		}
		
		.emaillabel{
			font-size:16px;
			height:25px;
		}
		
		#edituser{
			border-radius: 20px;
			float:right;
		}
		#uploadnewitem{
			border-radius: 20px;
			float:right;
		}
		
		.edititem{
			border-radius: 20px;
			font-size:10px;
			margin-right:10px;
		}
		.soldlabel{
			font-size:16px;
			font-weight:bold;
			height:25px;
		}
		.itemlabel2{
			margin-left: -30px;
			font-size:14px;
			height:20px;
		}
		
		#sort{
			float: right;
			margin-right:150px;
		}
		
		.titlelinkitem {
			background-color: white;
			border: 0px;
			padding: 10px 0px; 
			margin-left: 6px;
			font-family:"Verdana",sans-serif;
			color: #51B0B8;
			text-align: left;
			font-size:16px;
			font-weight:bold;
			cursor: pointer;
			margin-bottom:-15px;
			width:200px;
		}
		.titlelinkitem:hover {
			background-color: white;
		}
		.imagelinkitem {
			background-color: white;
			border: none;
			cursor: pointer;
			width:100px;
			height:120px;
			margin: 10px 30px 10px 10px;
		}
		td.emptyitem{
			
		}
		#radiobuttonpos2{
			position:absolute;
			top:140px;
			left:560px;
		}

		.reglabel{
			text-align:right;
			font-size:12px;
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
		</div>
	<?php }
	else{?>
	<div> <a href="Login.php" id="signin_reg">Login or Register</a>	</div>
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
	</div>
	<div id="main">
	<table><tr><td>
	<h1>User Profile</h1>
	<table class="contenttable">
		<tr>
		<td id='userinfo'>
		<h3>Personal Info <button id='edituser' onclick="changeEdit()" >Edit</button> </h3> 	
		</td>
		</tr>
		<tr>
		<td id='sellitems'>
		
		<h3>Your Uploaded Items <form name="upload" action="Upload.php" method="get">
		<input type="hidden" id="mode" name="mode" value="UploadItem"/>
		<button type="submit" id='uploadnewitem' style="float:right;">Upload a New Item</button></form> </h3> 
		
		<div id="sellitemsItems">
		</div>
		<br><center><button onclick=changeimage("sell",-1) >Previous</button><button onclick=changeimage("sell",1) >Next</button>
		<!--<br><div class="nextPrevImages" style="position:relative; width:10%; margin:auto;"><p><a href="#" id="prevSellImages">Previous</a> <a href="#" id="nextSellImages">Next</a></p></div>-->
		</td>
		</tr>
		<tr>
		<td id='biditems'>
		<h3>Your Leading Bids</h3>
		<div id="biditemsItems">
		</div>
		<br><center><button onclick=changeimage("buy",-1) >Previous</button><button onclick=changeimage("buy",1) >Next</button>
		<!--<br><div class="nextPrevImages" style="position:relative; width:10%; margin:auto; margin-bottom:50px;"><p><a href="#" id="prevBuyImages">Previous</a> <a href="#" id="nextBuyImages">Next</a></p></div>-->
		</td>
		
		</tr>
	</table>

	</tr></table>
	<form id="hiddenDeleteItem" action="UserProfile.php" method="get">
		<input type="hidden" id="deleteId" name="deleteId" value="" />
	</form>
	<form id="itemresult" action="ItemDescription.php" method="get">
		<input type="hidden" id="itemid" name="itemid" value="" >
	</form>
	<form id="hiddenEditItem" action="Upload.php" method="get">
		<input type="hidden" id="mode" name="mode" value="UpdateItem"/>
		<input type="hidden" id="itemId" name="itemId" value=""/>
	</form>
	
	</div>
	
	</body>
</html>