/* This header file is used to define the functions that is related to all the dates in this program such as
validation, output format etc */

#ifndef _date_h_
#define _date_h_

#include "std_lib_facilities.h"

class Date {
public:
	Date();							// default constructor
	Date(int dd, int mm, int yy);	// check for valid date and initialise
	int day() const;				// return the day
	int month() const;				// return the month
	int year() const;				// return the year

private:
	int y;
	int m;
	int d;
};

bool datevaild(int d, int m, int y); // datevalid means date validation, this boolean check for a valid date and return true if it is.

int daysinmonth(int y, int m); // the function check for the days in month

bool leapyear(int y); // this boolean check if y is a leap year and return true if it is

ostream& operator<<(ostream& os, const Date& d); // this overload operator<< will output a specific format for date

string printMonths(int m); // this will convert from integer month to a string and print it.

#endif 