<?php
	include "dbconnect.php";
	session_start();
	
	//check to see if the user has requested to logout. If so destroy their session.
	if(isset($_REQUEST['Logout'])){
		session_unset();
		session_destroy(); 
		//echo "All session variables are now removed, and the session is destroyed.";
	}
	
	//check to see if the user has requested to go to their profile page. Redirect them their if so
	if(isset($_REQUEST['UserProfile'])){
		header('Location: UserProfile.php');
	}

	//get the itemid of the item link that the user has pressed and wants to view that was passed from the previous page
	$itemId_passed = $_REQUEST['itemid'];
	
	//two SQL commands. The first selects the images to display. The second selects all information related to the item
	$sql ="SELECT image, MainImage FROM iBayImages WHERE itemId=".$itemId_passed." ORDER BY MainImage DESC";
	
	$sql2 = "SELECT * FROM iBayItems WHERE itemId=".$itemId_passed." ";

	//using the database connection $db, connect and query our SQL
	$res =& $db->query($sql2);
    
	//if we get an error from the query, output the error message the database sends back
	if (PEAR::isError($res)) {
		die($res->getMessage());
	}
	
	//declare an array to store the values that were returned from the query
	$Allresult = Array();
	
	//while we have results, put them into the array
	while ($result = $res->fetchRow()) {
		$result['description'] = htmlspecialchars($result['description'],ENT_QUOTES,'UTF-8');    //used to ensure the description displays correctly
		array_push($Allresult, $result);
	//$Allresult = $result;
}
//	$pre = $res->fetchAll();
	$result = json_encode($Allresult);     //encode the array such that we can use it within JavaScript and hence on the client side
		
	
	$t=time();
	
	//if the user is logged in declare a variable to store their username (used in case they make a bid)
	if(isset($_SESSION['username'])){
		$active_userId_passed = $_SESSION['username'];
	}else{
		$active_userId_passed = "";
	}

	//store the passed itemId
	$itemId_passed = $_REQUEST['itemid'];
	
	//if a bid was placed (then it has already been validated by JavaScript) so we can declare an SQL command to input into the database the updated price and highestBidder values
	if(isset($_REQUEST['place_bid'])){
		if(isset($_SESSION['username']) && $_SESSION['username']!="user"){
			$bidValue = $_REQUEST['bid_value'];  //get the bid value
			$query = "UPDATE iBayItems SET price=".$bidValue.",highestBidder='".$active_userId_passed."' WHERE itemId=".$itemId_passed."";
			
			//pass through to the database
			$res =& $db->query($query);
			//return error message if there is one			
			if (PEAR::isError($res)) {
				die($res->getMessage());
			}
			/*	
			if (mysqli_query($db, $query)) {
			} else {
				echo "Error updating record: " . mysqli_error($db);
			}
			*/
		}else{
			echo '<script>alert("You must be logged in to place a bid")</script>';
		}
	}
	
	//SQL to fetch all the seller information
	$sellerInfoSql = "SELECT members.name, members.address, members.postcode, members.rating FROM iBayMembers AS members INNER JOIN iBayItems AS items ON items.itemId=".$itemId_passed." AND items.userId=members.userId";
	$res_sellerInfo =& $db->query($sellerInfoSql);

	if (PEAR::isError($res_sellerInfo)) {
		die($res_sellerInfo->getMessage());
	}
	
	$pre_sellerInfo = $res_sellerInfo->fetchAll();
	$result_sellerInfo = json_encode($pre_sellerInfo);	   //again encode it so that we can refer to the values on client side

?>
<html>
    <head>
        <title>iBay ItemResults</title>
		<link type="text/css" rel="stylesheet" href="stylemain.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
		<script type='text/javascript'>
			var sql = "<?php echo $sql; ?>";
			var itemdescript = <?php echo $result; ?>;   //decode the encoded PHP array of item information array
			var currenttime = <?php echo $t; ?>;      //get the current time
			var str = itemdescript[0].finish;
			var timedate = str.replace(" ", "T"); 	//Setting the timedate into a suitable format so the javascript Date.parse will read it properly
			var imageArray = new Array();
			var startimage = 0;
			var endimage = 2;
			var lengthimage;
			
			var sellerinfo = <? echo $result_sellerInfo; ?>;                //decode the encoded PHP array of seller information array
			var usrname = '<?php echo $active_userId_passed; ?>';     //get the userId 
			
			//function which calculates the difference between current time and the finish time of the item (using milliseconds)
			function TimeRemains(endtime) {
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
			
			//function will create the timer, counting down the time remains for the item		
			function initializeClock(id, endtime) {
				var clock = document.getElementById(id);
				var daysSpan = clock.querySelector('.days');
				var hoursSpan = clock.querySelector('.hours');
				var minutesSpan = clock.querySelector('.minutes');
				var secondsSpan = clock.querySelector('.seconds');

				function updateClock() {
					var t = TimeRemains(endtime);

					daysSpan.innerHTML = t.days;
					hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
					minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
					secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

					//if the time difference is <=0 then item has finished.
					//so remove the countdown clock and bid box and bid button
					//replace the clock with a message to let user know item has ended
					if (t.total <= 0) {
						clearInterval(timeinterval);
						document.getElementById("clockdiv").innerHTML="";       //remove the clock
						document.getElementById("clockdiv").innerHTML="<span style='color:red;'>ITEM ENDED</span>";    //replace clock with this text
 						document.getElementById("bid_form").innerHTML="";       //remove bid box and the form in general so user cannot enter a new bid
	
					}
				}
				updateClock();
				var timeinterval = setInterval(updateClock, 1000);
			}

			//Getiting the time remaining for the item.
			var deadline = new Date(Date.parse(timedate));

			//JQuery to be executed on page load
			$(document).ready(function(){
				
				//Getting the images using ajax get function, senting the sql statement and store the images into an array.
				$.get("SearchQuery.php",{'sql':sql},function(JSONResult){ 
					for (var i = 0; i < JSONResult.length; ++i) {
						imageArray[i] = JSONResult[i].image;
					}
					lengthimage = imageArray.length;
					var html = "<td><center><img id='mainimgdata' src='data:image/jpeg;base64,"+imageArray[0]+"' style='height:360px;width:320px;'/></center></td>";  //coding the html for the main image
					$("#imagestable").append(html);	//Add the main image to the page
					
					createsubimg(startimage,endimage);	//Create the html code for the sub images
												
					},'json');		
				
				//the following is used to create the item's main information details which will displayed on the right-hand side of the images.
				//we create a variable 'item' and then keep appending to it the HTML code which is necessary
				//once we have all the HTML we need, we append all of this variable to the table data area with id='iteminfo'  using JQUery
				var item = "<br><h1 style='line-height:120%;'>"+itemdescript[0].title+"</h1>";
					item += "<h4>Time Left:<br><br><div id='clockdiv'><span class='days'></span> Days <span class='hours'></span> Hours <span class='minutes'></span> Minutes <span class='seconds'></span> Seconds </div></h3>";
					item += "<h4>Price: £"+itemdescript[0].price+"</h4>";
					item += "<div id='bid_form'><form name='bid_box' action='ItemDescription.php' method='get' onsubmit='return(validateBid("+itemdescript[0].price+"))';>";
				    item += '<h4><label class="itemlabel" for="PlaceBid">Place Bid: </label>£<input type="text" name="bid_value" id="bid_value" size="10" style="display:inline; margin-right:10px;" />';
					item += '<input type="hidden" id="itemid" name="itemid" value="<?php echo $itemId_passed; ?>" />';
					item += '<input type="hidden" id="username" name="username" value="<?php echo $active_userId_passed; ?>" />';
					item += '<input type="submit" name="place_bid" value="Place Bid " style="display:inline;" /></h4></form></div>';
					item += '<h4><label class="itemlabel" for="Postage">Postage: £'+itemdescript[0].postage+'</label></h4>';
				
				$("#iteminfo").append(item);			//Add the items information into the table
				
				//initialize the count down timer
				initializeClock('clockdiv', deadline);
				
				//similar to above, append the HTML for item description.
				var item_descr = "<h1>Description</h1>";
				item_descr += itemdescript[0].description+"<br><br>";
				
				$("#item_descr_place").append(item_descr);
				
				//append all the seller information
				var item_seller = "<h1>Seller Information</h1>";
				item_seller += "Seller Name: "+sellerinfo[0].name;
				item_seller += "<br>Address: "+sellerinfo[0].address;
				item_seller += "<br>Postcode: "+sellerinfo[0].postcode;
				item_seller += "<br>Seller Rating: "+sellerinfo[0].rating;
				
				$('#item_seller_place').append(item_seller);
				
				
			});		
			
			function changemainimg(x){ //this function with change the main image to a subimage when a subimage is clicked
				var image = "data:image/jpeg;base64,"+imageArray[x];
				$( "#mainimgdata" ).attr( "src", image );	//Changing the src of the main image			    
			}
			
			
			function createsubimg(x,y){ //Create the html code the for subimage in the table
			   $("#subimgsdata").remove();	//remove the data in the subimgsdata cell, if initialized.
				
				if (x != 0){	//if the subimages does not start with zero, it will display a dark green arrow with an onclick function so user can see previous images in the arrays.
					var html = "<tr id='subimgsdata'><td><img id='arrowleft' src='left_arrow.png' onclick=changesubimg('left') />";
				}
				else{		//A light green arrow with not functionality 
					var html = "<tr id='subimgsdata'><td><img id='arrowleft' src='left_arrow_no.png' />";
				}
				if (lengthimage < 3) {	//if the length of the image does not exceed three, we change the iteration for our loop to the image array length.
					y = lengthimage-1;
				}
				for (var i = x; i < y+1; ++i){ //looping the array coding the three images requested from x and y.
					html += "<img src='data:image/jpeg;base64,"+imageArray[i]+"' class='subimages' onclick=changemainimg("+i+") />";
				}
				if (endimage >= lengthimage-1){ //Adding the right arrow, if the array reaches the last three, show a light green arrow
					html += "<img id='arrowright' src='right_arrow_no.png' /></td></tr>";
				}
				else{ //Otherwise show a dark green arrow
					html += "<img id='arrowright' src='right_arrow.png' onclick=changesubimg('right') /></td></tr>";
				}
				
				$("#imagestable").append(html);		//Add the html code to the image table
			}

			function changesubimg(x){		//Function for changing the subimage, will run when the arrows are clicked.
				if(x == 'right'){			//Right arrow clicked, add one to the order of the image we are displaying
					startimage = startimage+1;
					endimage = endimage+1;
					createsubimg(startimage,endimage);	//Replace the images
				}
				if(x == 'left'){	//Left arrow clicked, subtract one to the order of the image we are displaying
					startimage = startimage-1;
					endimage = endimage-1;
					createsubimg(startimage,endimage);
				}
			}
			
			//function which validates an inputted bid when the user presses the 'Place Bid' button
			function validateBid(minBid){
				//check if the numerical value of the input is larger than the current price plus 5%
				ok=document.getElementById('bid_value').value >= minBid*1.05;	
				if(!ok){
					//if not alert user to bad bid
					alert("Bad Bid");
				}
				//ensure the user is logged in
				if(usrname==""){
					//if not alert them to this
					alert("Please sign in to bid.");
					return(false);
				}
				else{
					return(ok);
				}
							
				//return(ok);	
			}
			
		</script>
		<style>
		#item_images{
			position:relative;
			width:40%;
			height:675px;
			float: left;
			left:50px;
			background-color:white;
		}
		#itemtable{
			table-layout: auto;
		}
		#itemtable td{
			border: none;
			font-family:"Verdana", sans-serif;
			color:#20878E;
		}
		
		#imagestable{
			width:450px;
		}
		#imagestable td{
			border: 5px solid #51B0B8;
		}

		.subimages{
			height:140px;
			width:120px;
			padding:5px;
			border:0 none;
		}
		
		.subimagebutton{
			background-color: none;
			color: none;
			padding: 0px 0px; 
			border:0 none;
			cursor:pointer;
		}
		
		h4{
			color: #51B0B8;
			font-family:"Verdana",sans-serif;
			font-size:18px;
			font-weight:bold;
			text-align:left;
			line-height: 100%;
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
	<h1>Item Description</h1>
	<table id='itemtable' ><tr><td>
	<table id='imagestable'>
		<!--will store images -->
	</table>
	
	</td><td id='iteminfo' valign="top" style="width:75%;" ></td>     <!--will store main item information -->
	<tr><td colspan= 2 id="item_descr_place"></td></tr>   <!--will store item description -->
	<tr><td colspan= 2 id="item_seller_place"></td></tr>  <!--will store seller information -->

	</tr></table>
	</div>
	</body>
</html>