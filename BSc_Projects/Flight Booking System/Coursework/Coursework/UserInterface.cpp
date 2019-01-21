#include "std_lib_facilities.h"

#include "UserInterface.h"
#include "Date.h"

Date Inputdate; //An empty date variable
void setDate(Date& Date){ //This function will copy the date to the empty date variable above so I can use the date throughout this file
	 Inputdate = Date;
}

Date getDate(){ //This function will return the Inputdate and allow the function to use it.
	return Inputdate;
}

void start()	// Print the initial welcome message at the start of the program
{
	cout << setw(80) << setfill('-') << "-";
	cout << setw(28) << setfill('<') << "<";
	cout << left << setw(52) << setfill('>') << "Flight Booking System";
	cout << setw(80) << setfill('-') << "Created by Simon Yip" << endl;
	cout << "Welcome to the Flight Booking System" << endl;
	cout << "Please enter which function would you want?" << endl;
	cout << "(1) Book a Flight	(2) Display Flights from an Airport	  \n(3) Display all available Airports"<< endl;
	
}

void FindFlights()		//Run process for finding flights/searching for flight journeys
{
	cout << "Please Enter the airport you like to depart from: ";
	string Origin;
		cin >> Origin;
		checkCode(Origin); //Check if input code is valid (see DataConfig.cpp)
		

	cout << "Please Enter the Destination: ";
	string Dest;
		cin >> Dest;
		checkCode(Dest);
		
		
	int day, month, year;
	char a, b;
	
	cout <<"Please enter the date(dd/mm/yyyy) you want to leave: ";	
	cin >> day >> a >> month >> b >> year;
	Date DateofFlight(year,month,day);	//User input the date
	setDate(DateofFlight);				//Copying the DateofFlight to the variable "Inputdate" at the start of the cpp so we can use it later
		
	Search(Origin,Dest);				//Search Flights (see DataConfig.cpp)

	vector<Routes> initResult = getSearchR(); //Copy the information from SearchResult to vector "initResult"
	int size = initResult.size();
	if (initResult.size() == 0 || Origin == Dest){
		cout << "There is no Flight going from " << Origin << " to " << Dest << endl;
	throw 1;
	}
		else {
		cout << "\nHere are the list of available flights on " << DateofFlight << ":" << endl;
		int size = initResult.size();
		for (int i = 0; i<size; ++i){
			printresult(initResult,i);			//Display the result on the screen
			}
		}

	cout << "Would you like to sort flights by flight time or by cost:" << endl;
	cout << "(1) Time	(2) Cost	(3) Neither"<< endl;
	int Selection;
	cin >> Selection;
	if(!cin){
		throw runtime_error("Please enter a number");
	}
	switch (Selection) {
	case 1:
		bubblesortT(initResult);			//Bubblesort the result based on time
		for (int i = 0; i<size; ++i){
			printresult(initResult,i);		//Print sorted possible journey to screen
		}
		setSearchR(initResult);				//Update the result of bubblesort to vector<Routes>SearchResult
		ifBookYN();							//run ifBookYN function (see below)
	case 2:
		bubblesortC(initResult);			//Bubblesort the result based on Cost
		for (int i = 0; i<size; ++i){
			printresult(initResult,i);		//Print sorted possible journey to screen
		}
		setSearchR(initResult);
		ifBookYN();
	case 3:
		ifBookYN();
	default:
		cout << "Selection doesn't exist, proceed to Booking...\n";
		ifBookYN();
	}
}


void ifBookYN()				// A function that ask if user want to book a flight or not
{	
		cout <<"Would you like to book a flight? \n";
		cout << left << setw(11) << "Yes or No:";
		string bookflight;
		cin >> bookflight;

		if (bookflight == "Yes" || bookflight == "YES"|| bookflight == "yes"){ 
			Booking();
		}
		else if (bookflight == "No"|| bookflight == "NO" || bookflight == "no"){
			throw 1;
		}
		else {
			throw 'e';
		}
}
	
void Booking(){											// Run process for booking a flight.
	vector<Routes>finalResult = getSearchR();			// Copy from vector<Routes>SearchResults
	cout << "Please enter a number to select a flight from the list above:";
		int num;
		cin >> num;
		int flightnum = num - 1;
		if(!cin){
			throw runtime_error("Please enter a number to select the flight");
		}
		int size = finalResult.size();
		if (flightnum < 0 || flightnum > size ){	//Check if user chosen a vaild flightnumber
			throw runtime_error("Flight Option does not exist");
		}

		cout << "\nYou have selected this flight: \n\n";
		printresult(finalResult,flightnum);
	
		cout << "Enter Yes to confirm with the booking" << endl;
		cout << "Enter No if you want to cancel: ";
		string sele2;
		cin >> sele2;
	
		if (sele2 == "No"|| sele2 == "NO" || sele2 == "no"){
			throw 1;
		}
		else if (sele2 == "Yes"|| sele2 == "YES"|| sele2 == "yes"){
		printReceipt(finalResult, flightnum,getDate());			//Output the receipt of the booked flight to the screen

		ExportData(finalResult, flightnum,getDate());			//Exporting the receipt to a text file along with the date.

		cout << "Thank you booking a flight with us, " << endl;
		cout << "you will find a copy of the receipt in the project directory" << endl;
		throw 1;
		}
		else {
			throw 'e';
		}
}

void AirportStatus()		//Run process for searching Airport information
{
	cout << left << setw(35) << setfill('-') << "Search Airport info" << endl;
	cout << "Enter Airport Code : ";
	string acode;
	cin >> acode;
	checkCode(acode);		//Check if AirportCode is valid

	SearchAir(acode);		//Search for the Departures and Flights from the Airport
	AirportInfo(acode);		//Search for the Airport information

	DepArri();				//Output the search results to the screen
	
	throw 1;				
}