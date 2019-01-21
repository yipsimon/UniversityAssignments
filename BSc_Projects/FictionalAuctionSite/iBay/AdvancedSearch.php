<?php

session_start();
if(isset($_REQUEST['Logout'])){
		session_unset();
		session_destroy(); 
		//echo "All session variables are now removed, and the session is destroyed.";
}
if(isset($_REQUEST['UserProfile'])){
		header('Location: UserProfile.php');
}
?>
<html>
<head>

<title>Advanced Search Page</title>
<link type="text/css" rel="stylesheet" href="stylemain.css">
<script type="text/javascript"></script>
<style>
	.searchlabel{ 
		display:inline-block;
		font-size:14px;
		margin-right:10px;
	}
	
	.searchRlabel{
		display:inline-block;
		font-size:14px;
	}
	
	.searchtitle{
		font-size:18px;
		width:100px;
	}
	
	#itemtable{
		border: none;
		border-collapse: collapse;
		width: 1060px;
	}
	
	#itemtable td{
		border: none;
		border-collapse: collapse;
		font-family:"Verdana",sans-serif;
		padding:10px;
	}
	
</style>
</head>
<body>
<div>
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
		<a href="iBay-main.php">
			<center><img src="logo.png" alt="logo" style="width:180px;height:180px;border:0;"></center>
		</a>
	</div>
	<div id="main">
	<table><tr><td>
		<h1>Advanced Search</h1>
	<form name="advancesearch" action="SearchResults.php" method="get">
	<table id="itemtable"><tr><td>
	<!-- Creating the table and selection criteria -->
		<label class="searchtitle" for="Keywords">Keywords:</label><input type="text" name="keywords" size=70><br>
			<label class="reglabel" for="normal">Searching each individual Keywords:</label><input type="radio" name="regexpress" value="normal" checked> 
			<label class="reglabel" for="exact">Searching as exactly inputed:</label><input type="radio" name="regexpress" value="exact"> 
			<label class="reglabel" for="startwith">Searching Any items that start with these keywords:</label><input type="radio" name="regexpress" value="startwith"> 
			<label class="reglabel" for="endwith">Searching Any items that end with these keywords:</label><input type="radio" name="regexpress" value="endwith"> 
		</td></tr><tr><td>
		<label class="searchtitle" for="Category">Category:</label><br>
		<label class="searchlabel" for="All">All:</label><input type="radio" name="category" value="all" checked> 
		<label class="searchlabel" for="Clothing">Fashion:</label><input type="radio" name="category" value="Fashion"> 
		<label class="searchlabel" for="Sports">Sports:</label><input type="radio" name="category" value="Sports"> 
		<label class="searchlabel" for="Books">Books:</label><input type="radio" name="category" value="Books"> 
		<label class="searchlabel" for="Gaming">Gaming:</label><input type="radio" name="category" value="Gaming">
		<label class="searchlabel" for="Electronics">Electronics:</label><input type="radio" name="category" value="Electronics"> 

		<br><br></td><tr><td>
		<label class="searchtitle" for="Sort">Sort:</label><br>
		<label class="searchRlabel" for="NewestProducts">Newest Products:</label><input type="radio" name="sort" value="NewestProducts" checked> 
		<label class="searchRlabel" for="hightolow">High to Low:</label><input type="radio" name="sort" value="Pricehighlow"> 
		<label class="searchRlabel" for="lowtohigh">Low to High:</label><input type="radio" name="sort" value="Pricelowhigh">
		<label class="searchRlabel" for="EndingSoon">Ending Soon:</label><input type="radio" name="sort" value="EndingSoon">		<br>
		</td></tr><tr><td>
		<label class="searchtitle" for="Price">Price:</label><br>
		<label class="searchRlabel" for="Pricefrom">Price From:</label>
		<select name="pricef" >
			<option value=0 selected>0
			<option value=10 >£10+
			<option value=20 >£20+
			<option value=40 >£40+
			<option value=60 >£60+
			<option value=120 >£120+
			<option value=200 >£200+
		</select>
		<label class="searchRlabel" for="Priceto">Price To:</label>
		<select name="pricet">
			<option value=0 selected>Any
			<option value=10 >£10
			<option value=20 >£20
			<option value=40 >£40
			<option value=60 >£60
			<option value=120 >£120
			<option value=200 >£200
		</select>
		<br><br>
		</td></tr><tr><td>
		<label class="searchtitle" for="Postage">Postage:</label><br>
		<label class="searchRlabel" for="none">Doesn't matter:</label><input type="radio" name="postage" value="any" checked > 
		<label class="searchRlabel" for="Free">Free Postage:</label><input type="radio" name="postage" value="free"> 
		<label class="searchRlabel" for="NotFree">Charged Postage:</label><input type="radio" name="postage" value="notfree" > 
		<select name="postagecost">
			<option value=0 >£0+
			<option value=1 >£1+
			<option value=5 >£5+
			<option value=10 >£10+
		</select>
		
		<br><br>
		
		<input type="submit" name="advsearch" value="Search">
		
		</td></tr></table>
	</form>
	</td></tr></table>
<body>
</body>
</html>