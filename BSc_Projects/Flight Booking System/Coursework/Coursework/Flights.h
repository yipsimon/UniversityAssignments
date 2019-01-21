/* This header file "Flights.h" is created to solely contain the Flights Class
Similarly to Airport.h, the purpose of this class is to create a construtor of this class to use to read "flights.txt" file
record by record and store them in as one item in a vector*/

#ifndef _flights_h_ //In order to prevent double definitions.
#define _flights_h_

#include "std_lib_facilities.h"

class Flights
{
public:
	string OriginAir, DestAir, Airline;  // OriginAir means Original Airport, DestAir means Destination Airport
	int Price, Duration;

	Flights(string Origin, string Dest, string Line, int cost, int dur) // Construtor: following the same order as the file structure in "flights.txt."
		:OriginAir(Origin),DestAir(Dest),Airline(Line),Price(cost),Duration(dur){};
			// Origin will be stored as OriginAir, Dest will be stored as DestAir ...etc.
};

#endif 
