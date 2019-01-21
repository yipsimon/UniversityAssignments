/* This header file define all the functions used in data input and data output (see DataIO.cpp) */

#ifndef _DataIO_h_ //In order to prevent double definitions.
#define _DataIO_h_

#include "std_lib_facilities.h"
#include "Routes.h"		//Routes.h is included for the ExportData function
#include "Date.h"		//Date.h is included for for the ExportData function

void ImportData();		// This function combine ImportAirport() and ImportFlights() together and run them
void ImportAirport();	// This function will import all the data from "airports.txt" file 
void ImportFlights();	// This function will import all the data from "flights.txt" file
void ExportData(vector<Routes>& R, int C, Date DateofFlight);	// This function will export a receipt for the booking information

#endif 
