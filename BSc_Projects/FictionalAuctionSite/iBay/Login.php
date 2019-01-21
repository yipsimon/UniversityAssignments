<?php
	include "dbconnect.php";	//Connect to the database
	session_unset(); 			//Unset all the session variables
	session_start();			//Start a new session
	$invalid = 1;				//This variable is an indicator for the javascript error alert
	$log = -1;					//This variable is an indicator to distinguish which form or no form submitted
	if(isset($_REQUEST['Login'])){	//If Login is submitted, it will submit a sql query to check the database if the username and password matches in the database
		$log = 1;
		$user = $_REQUEST['username'];
		$pass = $_REQUEST['password'];
		$sql = "SELECT userId, password FROM iBayMembers WHERE userId='".$user."' AND password='".$pass."';";

		$res =& $db->query($sql);

		if (PEAR::isError($res)) {
			die($res->getMessage());
		}
		$pre = $res->fetchAll();
		$result = json_encode($pre);

		if(!empty( $pre )){		//If the sql query find a match in the database, it will change the error message and set the session varaible username to the input username.
			$invalid = 0;		
			$_SESSION['username'] = $user;
		}
	}
	if(isset($_REQUEST['Register'])){	//If Login is submitted, it will submit a sql query to insert into the database if the username is unqiue
		$log = 0;
		$reg2 = $_REQUEST['Register'];
		$user = $_REQUEST['newusername'];
		$pass = $_REQUEST['newpassword'];
		$sql2 = "SELECT userId FROM iBayMembers WHERE userId='".$user."';";		//sql query to check the inputted username is unique
		$res2 =& $db->query($sql2);

		if (PEAR::isError($res2)) {
			die($res->getMessage());
		}
		
		$row = $res2->fetchAll();
		$result2 = json_encode($row);

		if(empty( $row )){							//If the username is unique, we insert a new member into the database
			$name = $_REQUEST['name'];
			$email = $_REQUEST['Email'];
			$address = $_REQUEST['Address'];
			$post = $_REQUEST['Postcode'];

		$sql3 = "INSERT INTO `iBayMembers`(`userId`, `password`, `name`, `email`, `address`, `postcode`, `rating`) VALUES ('".$user."', '".$pass."', '".$name."', '".$email."', '".$address."', '".$post."', '1');";
		
		$res3 =& $db->query($sql3);
		
		if (PEAR::isError($res3)) {
			die($res->getMessage());
		}
			
		$invalid = 0;						//Set indicator for a different alert message
		
		$_SESSION['username'] = $user;		//Set the session variable username to the userid
		//$db->close();
		}
	}
	
?>
<html>
    <head>
        <title>ibay Login </title>
		<link type="text/css" rel="stylesheet" href="stylemain.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
		<script type='text/javascript'>
			$(document).ready(function(){
				var data = '<?php echo $log;?>';		//Getting the indicator for which form submitted
				var error = '<?php echo $invalid;?>';	//Getting the indicator for type of alert message.
				if (data == 1){							//If login form is submitted
					if (error == 1){					
						alert("Invalid login, please try again");		//Output the error message
						ErrorMsg("Invalid login, please try again");	//Set to show the error message in the login form
					}
					else {
						alert("Login Successful, redirecting to homepage");
						window.location.href = "iBay-main.php";			//Redirect to homepage if the login is successful
					}
				}
				if(data == 0){							//If the Registation form is submitted
					if(error == 1){
						alert("Username is already in used");		//Output the error message
						ErrorMsg2("Username is already in used");	//Set to show the error message in the register form
					}
					else {
						alert("Registation Successful, redirecting to homepage");	
						window.location.href = "iBay-main.php";		//Redirect to homepage if the register is successful
					}
				}					
			});				
			
			function valid(){								//This function checks if the passwords in the register form are equal to each other
				var pass1 = $("#newpassword").val();		//Getting the password
				var pass2 = $("#RPassword").val();			//Getting the repeated password
				if (pass1 == pass2){						//If the passwords are equal return true
					return true;
				}
				else{
					alert("Passwords do not match");		//Output error message
					return false;
				}
			}
			
		</script>
		<style>
		.addresslabel{
			margin-right:15px;
		}
		</style>
	</head>
	<body>
		<a href="iBay-main.php">
			<center><img src="logo.png" alt="logo" style="width:180px;height:180px;border:0;"></center>
		</a>
		<table class="logintable">
		<tr><td>
			<h2>Login</h2>
			<form id="login" action="Login.php" method="get"> <!--The Login form -->
			<label class="loginlabel" for="Username">Username:</label><input id="username" name="username" size="16"><br>
			<label class="loginlabel" for="Password">Password:</label><input type="Password" id="password" name="password" size="16"><br><br>
			<input type='submit' name="Login" id="Login" value='Login'>
			</form>
			<span class='errmsg' id='errmsg1'></span>	<!--All the span containing the errmsg class are all hidden until the jquery below shows it span along with the error message -->
			
		</td><td>
			<h2>Register</h2>
			<form id="Registation" action="Login.php" method="get" onsubmit="return valid();">	<!--The Registation form -->
			<fieldset style="text-align:left;">
				<legend>Personal information:</legend>
				<label class="loginlabel" for="Name">Name:</label><input name="name" size="16">
				<span class='errmsg' id='erm1'></span><br>
				<label class="loginlabel" for="Email">Email:</label><input type="email" name="Email" size="16">
				<span class='errmsg' id='erm2'></span><br>
				<label class="addresslabel" for="Address">Address:</label>
				<textarea style="margin:8px 0px 8px 0px;" name="Address" id="Address" rows="4" cols="40" maxlength="50"></textarea>
				<br><span class='errmsg' id='erm3'></span><br>
				<label class="loginlabel" for="Postcode">Postcode:</label><input name="Postcode" size="16">
				<span class='errmsg' id='erm4'></span><br>
			</fieldset><br>
			<fieldset>
				<legend>Create UserID:</legend>
				<label class="loginlabel" for="Username">Username:</label><input name="newusername" size="16"><br>
				<label class="loginlabel" for="Password">Password:</label><input type="Password" id="newpassword" name="newpassword" size="16"><br>
				<label id="exp" for="RPassword">Repeat Password:</label><input type="Password" id="RPassword" name="RPassword" size="16"><br>
			</fieldset><br>
			<input type="submit" name="Register" id="Register" value="Register">
			</form>
			<span class='errmsg' id='errmsg2'></span>
		</td></tr>
		</table>

		<script>
			$( "#login" ).submit(function( event ) {		//When the login form is submitted this jquery will run.
			if ($('[name="username"]').val() == "" || $('[name="password"]').val() == "") {	//This jquery will check for empty fields in the form,
				ErrorMsg("Received Empty input, please try again");							//If there exist an empty field, it will run this errormsg function
				event.preventDefault();			//Stop the form from submiting 
			}});
			
			$( "#Registation" ).submit(function( event ) {	//When the Registation form is submitted this jquery will run.
			if ($('[name="newusername"]').val() == "" || $('[name="newpassword"]').val() == ""  || $('[name="RPassword"]').val() == "" ) {	//Check if username, password and repeated password is empty
				ErrorMsg2("Received Empty input in userid section, please try again");	//If there exist an empty field, it will run this errormsg function
				event.preventDefault();
			}
			if($('[name="name"]').val() == "" ){	//Check if name is empty
				$("#erm1").text("Received Empty input, please try again").show();	//This will display error message in the span where id is erm1.
				event.preventDefault();
			}
			if($('[name="Email"]').val() == "" ){	//Check if email is empty
				$("#erm2").text("Received Empty input, please try again").show();	//Similar functionality but with different id. 
				event.preventDefault();
			}
			if($('[name="Address"]').val() == ""){	//Check if address is empty	
				$("#erm3").text("Received Empty input, please try again").show();
				event.preventDefault();
			}
			if($('[name="Postcode"]').val() == ""){	//Check if postcode is empty
				$("#erm4").text("Received Empty input, please try again").show();
				event.preventDefault();
			}
			});
			function ErrorMsg(Error){				//This error function will show the error message in the login form
				$("#errmsg1").text(Error).show();
			};
			
			function ErrorMsg2(Error){				//This error function will show the error message in the Registation form
				$("#errmsg2").text(Error).show();
			};
			
		</script>
	</body>
</html>
