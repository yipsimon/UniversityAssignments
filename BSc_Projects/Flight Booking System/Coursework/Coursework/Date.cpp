#include "std_lib_facilities.h"
#include "Date.h"

Date::Date() // default constructor - set to 1/1/2000
	:y(2000), m(1), d(1) {}

Date::Date(int yy, int mm, int dd) // check for valid date and initialise
	:y(yy), m(mm), d(dd)
{
	if (!datevaild(y, m, d))
		error("Invalid date, please try again");
}

int Date::day() const		//return the day
{
	return d;
}

int Date::month() const		//return the month
{
	return m;
}

int Date::year() const		//return the year
{
	return y;
}

bool datevaild(int y, int m, int d) // returns true for valid date
{
	if (y<2015 || y>2100)
		return false;
	if (d<=0 || d>daysinmonth(y,m))
		return false;
	if (m<=0 || m>12)
		return false;

	return true;
}

int daysinmonth(int y, int m)		//Check the days in the each month
{
	switch (m) {
			case 2:
					return (leapyear(y))?29:28; // the length of February varies
			case 4: case 6: case 9: case 11:
					return 30;
			default:
					return 31;
		}
}

bool leapyear(int y) // returns true if y is a leap year
{
	// any year divisible by 4 except centenary years not divisible by 400
	if (y%4!=0)
			return false;
	if (y%100==0 && y%400!=0)
			return false;
	return true;
}

string printMonths(int m){   //Convert and print month as string
	vector<string> Months;
	Months.push_back("January"); Months.push_back("February"); Months.push_back("March"); Months.push_back("April"); 
	Months.push_back("May"); Months.push_back("June"); Months.push_back("July"); Months.push_back("August"); 
	Months.push_back("September"); Months.push_back("October"); Months.push_back("November"); Months.push_back("December"); 

	return Months[m-1];

}

ostream& operator<<(ostream& os, const Date& d) //Setting a standard format for outputting a date class.
{
	return os << d.day() << " " << printMonths(d.month()) << " " << d.year();
}
