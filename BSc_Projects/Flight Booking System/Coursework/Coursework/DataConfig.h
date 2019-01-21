/* This header file is used to define all the functions (except the ones in UserInterface & Date) 
that I will be using in this project that involve Data Configuration hence it is called DataConfig */

#ifndef _DataConfig_h_ //In order to prevent double definitions.
#define _DataConfig_h_

#include "std_lib_facilities.h"
#include "Flights.h"	//To use the Flights class
#include "Airports.h"	//To use the Airports class
#include "Routes.h"		//To use the Routes class
#include "Date.h"		//To use the Date for printReceipt function.


void setAirportR(vector<Airports>& R);		// This copy all the elements from some vector<Airports> to a vector called vector<Airports> AirportRecords (located in DataConfig.cpp).

vector<Airports>& getAirportR();			// This will get a copy of the vector<Airports> AirportRecords to another vector<Airports>
	
void setFlightR(vector<Flights>& R);		// Same as setAirportR() but with Flights and to vector<Flights>FlightRecords

vector<Flights>& getFlightR();				// Same as getAirportR() but with Flights

void setSearchR(vector<Routes>& R);			// Same as setAirportR() but with Routes and to vector<Routes>SearchResults

vector<Routes>& getSearchR();				// Same as getAirportR() but with Routes

void Search(string Origin, string Dest);	// This is a Search function which will search all the possible journey available and store them in some vector<Routes>.

void swap(int& a,  int& b);					// A swap function needed to complete the bubblesort algorthm.

void bubblesortC(vector<Routes>& v);		// A bubblesort Algorthm for Cost from low to high

void bubblesortT(vector<Routes>& v);		// A bubblesort Algorthm for time from short to long. 

void printresult(vector<Routes>& R,int i);	// A function to print out the search result (all the records from vector<Routes> SearchResults)

void SearchAir(string Code);				// A function to search all the Arrival and Departure flights based on the string and store them respective flight vectors.

void setDepartFlig(vector<Flights>& R);		// This copy all the elements from some vector<Flights> to a vector called vector<Flights> DepartFlight (DepartFlight means Departure Flights and it is located in DataConfig.cpp).

vector<Flights>& getDepartFlig();			// This will get a copy of the vector<Flights> DepartFlight to another vector<Flights>

void setArriFlig(vector<Flights>& R);		// Similar to setDepartFlig() but with vector<Flights> ArriFlight (ArriFlight means Arrival Flights and it is located in DataConfig.cpp).

vector<Flights>& getArriFlig();				// Same as getDepartFlig() but with vector<Flights> ArriFlight

void AirportInfo(string acode);				// A function which will search and display all the information about the inputed airport (from string acode)

void DepArri();								// A function which print out all the results from vector<Flights> ArriFlight and vector<Flights> DepartFlight

void printReceipt(vector<Routes>& R, int i, Date IDate);		// A function which will print out the receipt of the booked flight

void checkCode(string a);					// A function which check whether the entered AirportCode is valid and existed in the system

void DisplayCode(); 

#endif