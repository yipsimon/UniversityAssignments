/* This header file "Airports.h" is created to solely contain the Airports Class
This purpose of this class is to create a construtor of this class as use to read "airports.txt" file
record by record and store them in as one item in a vector*/

#ifndef _airports_h_ //In order to prevent double definitions.
#define _airports_h_ 

#include "std_lib_facilities.h" // Include some declaration of C++ Standard Library etc <iostream>, <vectors>, <string> etc

class Airports 
{
public:
	string AirportCode,AirportName; 
	int DepartTax,ConnectTime;	// DepartTax is Departure Tax and ConnectTime is Connection Time

	Airports(string Code, string Name,  int Tax, int Time)	// Construtor: following the same order as the file structure in "airports.txt".
		:AirportCode(Code),AirportName(Name),DepartTax(Tax),ConnectTime(Time){};	
			// Code will be stored as AirportCode, Name will be stored as AirportName ...etc.

};

#endif 