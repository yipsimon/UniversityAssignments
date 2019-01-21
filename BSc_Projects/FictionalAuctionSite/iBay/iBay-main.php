<?php
session_start();

//has the user pressed to logout. If so, destroy the session
if(isset($_REQUEST['Logout'])){
		session_unset();
		session_destroy(); 
		//echo "All session variables are now removed, and the session is destroyed.";
}
//if the user has pressed the Your Accout  button send them there
if(isset($_REQUEST['UserProfile'])){
		header('Location: UserProfile.php');
}
?>
<html>
<head>

	<title>Homepage</title>
<link type="text/css" rel="stylesheet" href="stylemain.css">
<script type="text/javascript">



</script>
<style>
#radiobuttonpos{
	position:absolute;
	top:295px;
	left:660px;
}

.homelabel{
	text-align:right;
	font-size:12px;
}

</style>
</head>
<body>
<?php 
	//if the username is set ie)they are logged in
	if(isset($_SESSION['username']) && $_SESSION['username']!= "user" ){
	?>
		<div id="loggedon">
		<form action="iBay-main.php" method="get">
		<!--add buttons to user profile and one to logout and send the user to the respective pages if they press one-->
		<input type="submit" class="user_logged" name="UserProfile" value="Your Account">
		<input type="submit" class="user_logged" name="Logout" value="Log Out">
		</form>
		</div>
	<?php }
	//if they are not logged in
	else{?>
	<div>
		<!-- add a login or register button -->
		<a href="Login.php" id="mainsignin_reg">Login or Register</a>	</div>
	<?php } ?>
		<div style="position:absolute; top:70px; left:40px;">
		<!-- add the logo -->
		<a href="iBay-main.php" ><img src="logo.png" width="300"></a>
		</div>
		<div id="mainnav">
		<!-- set up the nav bar. Send the input of user and the user to SearchResults.php on pressing of one of the buttons -->
		<form name="defaultsearch" action="SearchResults.php" method="get">
		<ul id="mainnavbar">
			<!-- add the category buttons for the nav bar -->
			<li><input type="submit" class="mainnavElement" name="search_default" value="Fashion" /></li>
			<li><input type="submit" class="mainnavElement" name="search_default" value="Sports" /></li>
			<li><input type="submit" class="mainnavElement" name="search_default" value="Books" /></li>
			<li><input type="submit" class="mainnavElement" name="search_default" value="Gaming" /></li>
			<li><input type="submit" class="mainnavElement" name="search_default" value="Electronics" /></li>
		</ul>
		</form>
		</div>
		<!-- add the search bar; send the user and search variables to SearchResults.php on submit -->
		<form name="mainsearch" action="SearchResults.php" method="get">
			<input type="text" id="mainsearchbar" name="search_input" placeholder="What are you looking for..." size="70"/>
			<input type="submit" id="mainsearchbutton" value="Search it..." />
		</form>
			<!-- add button so user can do an advanced search -->
			<a id="mainadv" href="AdvancedSearch.php">Advanced Search</a>

</body>

</html>