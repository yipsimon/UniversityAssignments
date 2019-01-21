#include "std_lib_facilities.h"
#include "DataIO.h"
#include "DataConfig.h"
#include "UserInterface.h"

void main()
try{
	ImportData();	//Import all data from files.
	start();		//Print the initial welcome message at the start of the program

	int function;
	cin >> function;

	if(!cin){
		throw runtime_error("Please enter a number"); // Throw runtime_error if the input is anything other then integer
	}
	switch (function) {
		case 1:
			cin.ignore(numeric_limits<streamsize>::max(), '\n'); // This line ignores the rest of the current line, up to '\n':
																 // The numeric_limits<streamsize>::max() sets the maximum number of characters to ignore which there is no limit.
			FindFlights();										 // Run process for finding flights
		case 2:
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			AirportStatus();									 // Run process for searching Airport information
		case 3:
			DisplayCode();
		default:
			throw runtime_error("Function doesn't exist please try again");	// Throw runtime_error is input is anything other than 1 or 2
	}
}
catch(runtime_error& e){					//Catch all runtime_error from above, including throws within the functions
	cerr << e.what() << endl << endl;		//Print the string within runtime_error
	cerr << "restart..." << endl;
	cin.clear();							//Clear errors
	cin.ignore(numeric_limits<streamsize>::max(), '\n');
	main();									//run the main function, effectively rerunning the program again
}
catch(int){								//Catch all integer type throw error
	cerr << "Enter (1) to restart or any character to End Program" << endl;
	cin.clear();
	cin.ignore(numeric_limits<streamsize>::max(), '\n');
	int sele1;
	cin >> sele1;
	switch (sele1){
	case 1:									//if sele1 = 1, rerun the program again
		main();
	default:
		return;								//End Program
	}
}
catch(char){								//Catch all character type throw error
	cout << "Invalid selection, enter any character to end program";		
	cin.clear();
	cin.ignore(numeric_limits<streamsize>::max(), '\n');
	char c;
	cin >> c;
	return;
}
catch (exception& e) {						//Catch all generic exceptions
cerr << "error: " << e.what() << endl;
keep_window_open("q");
return;
}
catch (...) {								//Catch all other exceptions
cerr << "oops Esome unknown exception" << endl;
keep_window_open("q");
return;
}
