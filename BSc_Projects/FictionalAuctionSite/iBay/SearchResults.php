<?php
	session_start();		//Start the session, making the session variables available in this page

//If user click the logout button, it will run this
if(isset($_REQUEST['Logout'])){	//The logout button is of type=submit, we can check if it is requested
		session_unset();	//All session variables are now removed
		session_destroy();  //The session is destroyed.
}

//If the user click "My account" buttom, it will redirect them to the UserProfile page
if(isset($_REQUEST['UserProfile'])){
		header('Location: UserProfile.php');
}

//If the user click one of the category on the navigation bar, it will construct this sql statement
if(isset($_REQUEST['search_default'])){
	$sort = "NewestProducts";
	$search = strtolower($_REQUEST['search_default']);	//Making the value into lowercase
	//This sql statement is for searching all items that in the one of the category
	$sql = "SELECT * From iBayItems LEFT JOIN iBayImages ON iBayItems.itemId = iBayImages.itemId WHERE Mainimage = 1 AND category = '".$search."' AND finish > now() ORDER BY iBayItems.itemId DESC ;";
}

//If the user search from the simple text box, it will construct a different sql statement
if(isset($_REQUEST['search_input'])){
		$sort = "NewestProducts";
		$search = $_REQUEST['search_input'];  //Getting the string from the search box.
	
		//This piece of code will get rid of whitespaces at the end
		$length = strlen($search)-1;			//Get length of search
		$lastspace = strripos($search, ' ');	//Get last position of whitespaces
		if( $length == $lastspace){				//If whitespace is located at the end of string
			$rest = substr($search, -1);		//Get last character of string 
			$x = 0;
			while($rest === ' '){				//If last character of string is a whitespace
				$search = substr($search,0,$length+$x);	//Get rid of the whitespace at the end
				$rest = substr($search, -1);		//Check if last character of new string is whitespace
				$x = $x-1;						//if white space, loop again, decreasing string by one again
			}
		}
		
		//Copy the search string
		$content = $search;	
		$content2 = $search;
		
		//This code below will break the search string and store them into three arrays
		$num = substr_count($content, ' ');	//Counting the number of space inbetween the search string
		$keyword = Array();		//This array store all individual words from the search string
		$partword = Array();	//This array store sentences of the search string by taking away a word from the right
		$partword2 = Array();	//This array store sentences of the search string by taking away a word from the left
		$start = 0;
		array_push($partword2, substr($content, 0)); 
		//For loop that loop from the number of space it has in the search string
		for ($i=0; $i< $num; $i++){
			$pos = strpos($content,' ');
			$pos2 = strrpos($content2,' ');
			array_push($keyword, substr($content, $start, $pos));
			$content = substr($content, $pos+1);
			$content2 = substr($content2, $start, $pos2);
			array_push($partword, $content);
			array_push($partword2, $content2);
		}
		array_push($keyword, $content);
		array_pop($partword);
		array_pop($partword2);

		//Merging the words and sentences into a new array
		$result = array_merge($partword2, $partword); 
		$result = array_merge($result, $keyword);
	
		//Setting the initial sql statement to get all items with their main images
		$sql = "SELECT * From iBayItems LEFT JOIN iBayImages ON iBayItems.itemId = iBayImages.itemId WHERE Mainimage = 1 ";
		
		//If the array of all the words and sentences are not empty than concatenate the sql statement with further conditions 
		if( $result[0] != ""){
			$sql = $sql."AND ( title LIKE '%".$result[0]."%'";	//Condition: if the title of items match or similar to the word or sentence
			for ($k = 1; $k < count($result); $k++){			//Loop adding more condition if array are greater than one
				$sql = $sql."OR title LIKE '%".$result[$k]."%' ";
			}	
			$sql = $sql.") OR ( category = '".$result[0]."' ";	//Condition: if the category matches any of the word or sentences 
			for ($k = 1; $k < count($result); $k++){			//Looping more condition if there is more words or sentences.
				$sql = $sql."OR category = '".$result[$k]."' ";
			}
			$sql = $sql." ) ";	//Close this part of the condition
		}
		$sql = $sql."AND finish > now() ORDER BY iBayItems.itemId DESC ; ";	//Finally finishing the sql statement with greater than current time and order by lastest upload.
}

//If the user searched from the advance search page, it will check whether the value from the submit button of the advance search page can be selected, and construct a even more complex sql statement
if(isset($_REQUEST['advsearch'])){
	//Extracting all the input elements from the advance search form.
	$keywords = $_REQUEST['keywords'];		
	$category = $_REQUEST['category'];
	$sort = $_REQUEST['sort'];
	$pricef = $_REQUEST['pricef'];
	$pricet = $_REQUEST['pricet'];
	$postage = $_REQUEST['postage'];
	$postagecost = $_REQUEST['postagecost'];
	$expression = $_REQUEST['regexpress'];
	$sql = "SELECT * From iBayItems LEFT JOIN iBayImages ON iBayItems.itemId = iBayImages.itemId WHERE Mainimage = 1 ";

	//Add category condition if it is selected
	if($category != "all"){
		$sql = $sql."AND category = '".$category."' ";	
	}	
	
	//Add price condition, for all item that is greater then this price
	if($pricef != 0){
		$sql = $sql."AND price >= ".$pricef." ";	
	}
	
	//Add price condition, for all item that is less then this price
	if($pricet != 0){
		$sql = $sql."AND price <= ".$pricet." ";		
	}

	//If free postage is selected, add this condition
	if($postage === "free"){
		$sql = $sql."AND postage = 0 ";
	}
	
	//If postage is not free, add this condition
	if($postage === "notfree"){
		$sql = $sql."AND postage >= ".$postagecost." ";
	}

	//Check if keyword is inputted, and add the relevant sql condition
	if(!empty($keywords)){
	
	//The user can select how to search the database with their keywords, for normal, it will run the same way as a search bar (see above)
	if($expression === 'normal'){
		$search = $keywords;
		$content = $keywords;
		$content2 = $keywords;
	
		$num = substr_count($content, ' ');
		$keyword = Array();
		$partword = Array();
		$partword2 = Array();
		$start = 0;
		array_push($partword2, substr($content, 0));
		for ($i=0; $i< $num; $i++){
			$pos = strpos($content,' ');
			$pos2 = strrpos($content2,' ');
			array_push($keyword, substr($content, $start, $pos));
			$content = substr($content, $pos+1);
			$content2 = substr($content2, $start, $pos2);
			array_push($partword, $content);
			array_push($partword2, $content2);
		}
		array_push($keyword, $content);
		array_pop($partword);
		array_pop($partword2);
		
		$result = array_merge($partword2, $partword);
		$result = array_merge($result, $keyword);	
		
		$sql = $sql."AND (title LIKE '%".$result[0]."%' ";
		for ($k = 1; $k < count($result); $k++){
			$sql = $sql."OR title LIKE '%".$result[$k]."%' ";
		}
		$sql = $sql.") ";
	}	
	
	//If the user select to search the exact words, it will search for a title that is idential to the string input.
	if($expression === 'exact'){
		$sql = $sql."AND title = '".$keywords."' "; //This is the sql condition for this
	}
	
	//It will search for title that start with the string input
	if($expression === 'startwith'){
		$sql = $sql."AND title LIKE '".$keywords."%' "; //the % symbol on the right give this condition
	}
	
	//It will search for title that end with the string input
	if($expression === 'endwith'){
		$sql = $sql."AND title LIKE '%".$keywords."' "; //the % symbol on the left give this condition
	}	
	}
	$sql = $sql."AND finish > now() ORDER BY iBayItems.itemId DESC ; "; //Close the sql statement
}
?>
<html>
    <head>
        <title>iBay ItemResults</title>
		<link type="text/css" rel="stylesheet" href="stylemain.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
		<script type='text/javascript'>
			var sql = "<?php echo $sql;?>";			//Getting the SQL statement from php
			var sorting = "<?php echo $sort; ?>";	//Getting the sort value from php
			var JSONitems = new Array();	
			var Original = new Array();
			
			
			$(document).ready(function(){
				
				$.get("SearchQuery.php",{'sql':sql},function(JSONResult){ 
						if(JSONResult.length > 0){
							JSONitems = $.extend(true, {}, JSONResult);	//Copy the query results
							Original = $.extend(true, {}, JSONResult);	//Same here
							$('#initialRow').remove();					//Remove the initialrow in the itemtable
							createtable(JSONResult);					//create the rows to display the query results in
							$('#sort').val(sorting);					//Setting the Sort of the results
							
						}	
						else{
								$('#initialRow').remove();				//Remove the initialrow in the itemtable
								var html = "<tr id='initialRow'><td>No Matching Results.</td></tr>";	//HTML for displaying no match results
								$("#itemtable").append(html);			//Add the HTML code to the itemtable
						}
					},'json');		
				});		
			
			//This function will iterate the JSON Object array and add their value into the html code and add it to the itemtable
			function createtable(data){
				$.each(data, function ( index, value ) { //This is the iteration function
					var html =  "<tr class='itemresult'><td>";	//Open table cell
						html += "<img class='imagelink' src='data:image/jpeg;base64,"+value.image+"' width='185px' height='200px' onclick=itemlink("+value.itemid+") />";	//Displaying the image
						html += "<button class='titlelink' onclick=itemlink("+value.itemid+") >"+value.title+"</button>";	//Displaying the title
						html += "<ul class='noliststy' ><li><label class='itemlabel' for='Category'>Category :</label>"+value.category+"</li>"; //Displaying the category
						html += "<li><label class='itemlabel' for='Price'>Price :</label>"+"£"+value.price+"</li>";		//Displaying the price
						html += "<li><label class='itemlabel' for='Postage'>Postage :</label>"+"£"+value.postage+"</li>";	//Displaying the postage price
						html += "<li><label class='itemlabel' for='BidEnding'>Bid Ending in</label>"+value.finish+"</li>";	//Displaying the finish time for the item
						html += "</ul></td></tr>";		//Close table cell
					$("#itemtable").append(html);		//Add the html code to the itemtable
				});
			}
			
			function itemlink(x){	//Store the variable into itemid in the hidden from and submit it
				$("#itemid").val(x);
				document.getElementById("itemresult").submit();
			}
			
			function TimeRemains(endtime) {	//Takes a given time and calculate the time remain from today to reach the given time. 
				var t = Date.parse(endtime) - Date.parse(new Date());	
				var seconds = Math.floor((t / 1000) % 60);
				var minutes = Math.floor((t / 1000 / 60) % 60);
				var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
				var days = Math.floor(t / (1000 * 60 * 60 * 24));
				return {					//The function can return as total(milliseconds), days, hours, minutes or seconds
					'total': t,
					'days': days,
					'hours': hours,
					'minutes': minutes,
					'seconds': seconds
				};
			}
			
			function sortTable(x){	//This function will sort the exist item tables cell.
				var i,j,min,max;
				var temp = {};
				if(x == "NewestProducts"){	//If the function is given "NewestProducts", it will display the data as we first started
				$('.itemresult').remove();	//Remove the current data
					createtable(Original);	//Append the original data that we copied before from JSONResult
				}
				 
				if (x == "Pricehighlow"){	//If the function is give "Pricehighlow", it will display the data from high price to low.
					for (i = 0; i < Object.keys(JSONitems).length - 1; ++i) {	//Looping through the JSONitems array
						max = i;
                        for (j = i + 1; j < Object.keys(JSONitems).length; ++j) {	//Finding the highest price
                            if (parseFloat(JSONitems[max].price) < parseFloat(JSONitems[j].price)) {
								max = j;
                            }
						}
						//Swapping the items around in the array
						temp = JSONitems[i];
						JSONitems[i] = JSONitems[max];
						JSONitems[max] = temp;
					}
					$('.itemresult').remove();	//Remove the data after sort
					createtable(JSONitems);		//Adding the data array that we have sorted
				}
				
				if(x == "Pricelowhigh"){	//If the function is give "Pricelowhigh", it will display the data from low price to high.
					for (i = 0; i < Object.keys(JSONitems).length - 1; ++i) {	//Again looping through the JSONitems array
						min = i;
                        for (var j = i + 1; j < Object.keys(JSONitems).length; ++j) {	//Finding the lowest price
							if (parseFloat(JSONitems[j].price) < parseFloat(JSONitems[min].price)) {
								min = j;
                            }
						}
						//Swapping the items around in the array
						temp = JSONitems[i];
						JSONitems[i] = JSONitems[min];
						JSONitems[min] = temp;
					}
					$('.itemresult').remove();	//Remove the data after sort
					createtable(JSONitems);	//Adding the data array that we have sorted
				}
				
				if(x == "EndingSoon"){	//If the function is give "EndingSoon", it will display the data that is closest to the current date
					for (i = 0; i < Object.keys(JSONitems).length - 1; ++i) {	//Same loop as before
						min = i;
                        for (var j = i + 1; j < Object.keys(JSONitems).length; ++j) {
							var str1 = JSONitems[min].finish;			//Format is i.e. 2016-05-31 00:00:00
							var timedate1 = str1.replace(" ", "T"); 	//This time when we are getting the finish time of the item, we need to replace the whitespace in the data with T, in order for the TimeRemains function to read the finish time properly
							var str2 = JSONitems[j].finish;
							var timedate2 = str2.replace(" ", "T"); 	//Same here
							if (parseInt(TimeRemains(timedate2).days) < parseInt(TimeRemains(timedate1).days)) {	//Comparing days first
									min = j;
                            }
							else if(parseInt(TimeRemains(timedate2).days) == parseInt(TimeRemains(timedate1).days)) {	//If the days are equal, compare hours
								if(parseInt(TimeRemains(timedate2).hours) < parseInt(TimeRemains(timedate1).hours)) {
									min = j;
								}
								else if(parseInt(TimeRemains(timedate2).hours) == parseInt(TimeRemains(timedate1).hours)){	//If the hours are equal, compare minutes
									if(parseInt(TimeRemains(timedate2).minutes) < parseInt(TimeRemains(timedate1).minutes)) {
										min = j;
									}
								}
							}
						}
						//Swapping the items around in the array
						temp = JSONitems[i];
						JSONitems[i] = JSONitems[min];
						JSONitems[min] = temp;
					}
					$('.itemresult').remove(); //Remove the data after sort
					createtable(JSONitems);	//Adding the data array that we have sorted
				}
			}
			
		</script>
		<style>
		.noliststy{
			list-style-type: none;
		}
		#itemtable{
			border: none;
			border-collapse: collapse;
			width: 1060px;
		}
		#itemtable td{
			border: none;
			border-collapse: collapse;
			color: #51B0B8;
			font-family:"Verdana",sans-serif;
			padding:10px;
		}
		.itemlabel{
			font-size:16px;
			width:120px
		}
		#sort{
			float: right;
			margin-right:150px;
		}
		
		.titlelink {
			background-color: white;
			border: none;
			margin-left: -24px;
			font-family:"Verdana",sans-serif;
			color: #51B0B8;
			text-align: left;
			font-size:24px;
			font-weight:bold;
			cursor: pointer;
		}
		.titlelink:hover {
			background-color: white;
		}
		.imagelink {
			background-color: white;
			border: none;
			cursor: pointer;
			
			float: left;
			display: inline block;
			border: 1px dotted black;
			margin: 0px 30px 15px 10px;
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
	<h1>Search Results</h1>
	<br><select id="sort" onchange="sortTable(document.getElementById('sort').value)"> <!-- This is the drop down box for selecting the sorting -->
		<option value="NewestProducts">Newest Products
		<option value="Pricehighlow">Price High-Low
		<option value="Pricelowhigh">Price Low-High
		<option value="EndingSoon">Ending Soon
		
	</select>
	
	<table id="itemtable">	<!-- This is the table where we insert html code from javascript and displays the searched items -->
		<tr id="initialRow"><td>Loading...</td></tr>
	</table>
	
	</td></tr></table>
	</div>
	<form id="itemresult" action="ItemDescription.php" method="get">  <!--From the itemlink function, this form will be give an itemid to pass through to the ItemDescription page -->
		<input type="hidden" id="itemid" name="itemid" value="" >
	</form>
	
	</body>
</html>
