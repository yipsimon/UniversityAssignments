/* This header file is used to define the functions that are in UserInerface.cpp and Main.cpp */

#ifndef _UserInterface_h_ //In order to prevent double definitions.
#define _UserInterface_h_

#include "std_lib_facilities.h"
#include "DataConfig.h"
#include "DataIO.h"

void start(); // Print the initial welcome message at the start of the program
void FindFlights(); //Run process for finding flights/searching for flight journeys
void AirportStatus(); //Run process for searching Airport information
void ifBookYN(); // A function that ask if user want to book a flight or not
void Booking(); // Run process for booking a flight.
void setDate(Date& Date); // Copy the date from another function and store it in Inputdate (see UserInterface.cpp)
Date getDate(); // Return the Inputdate

#endif