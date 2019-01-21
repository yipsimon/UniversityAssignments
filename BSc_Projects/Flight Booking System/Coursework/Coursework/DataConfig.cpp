#include "std_lib_facilities.h"

#include "DataConfig.h"

vector<Airports> AirportRecords;
vector<Flights> FlightRecords;
vector<Flights> DepartFlight;
vector<Flights> ArriFlight;
vector<Routes> SearchResults;

void setAirportR(vector<Airports>& R){ // This copy all the elements from some vector<Airports> to vector<Airports> AirportRecords, mainly use to update the vector.
	AirportRecords = R;
}

vector<Airports>& getAirportR(){ // This will get a copy of the vector<Airports> AirportRecords to another vector<Airports>, allow the data from the vector to be used while keeping the original vector
	return AirportRecords;
}

void setFlightR(vector<Flights>& R){ //Similar to setAirportR
	FlightRecords = R;
}

vector<Flights>& getFlightR(){
	return FlightRecords;
}

void setSearchR(vector<Routes>& R){
	SearchResults = R;
}

vector<Routes>& getSearchR(){
	return SearchResults;
}

void setDepartFlig(vector<Flights>& R){
	DepartFlight = R;
}

vector<Flights>& getDepartFlig(){
	return DepartFlight;
}

void setArriFlig(vector<Flights>& R){
	ArriFlight = R;
}

vector<Flights>& getArriFlig(){
	return ArriFlight;
}

/* This is a Search function which will search all the possible journey available and store them in some vector<Routes>. 
By using multiple "for" loop, i can look through the vector<Flight> Flight until i find a a journey that matches the inputed Origin and Destination Airport.
For example when looking for flight connection, if loop one equal to Origin and loop two equal to Destination and loop one Destination equal loop two Origin, flights can be connected.*/
void Search(string Origin, string Dest){ 
	vector<Flights> Flight = getFlightR();
	vector<Airports> Air = getAirportR();
	vector<Routes> Temp3;
	int size = Flight.size();
	for(int i = 0; i<size; i++) 
		while (Origin == Flight[i].OriginAir && Dest ==  Flight[i].DestAir){ 
			Temp3.push_back(Routes(Flight[i].OriginAir,Flight[i].OriginAir," "," ",Flight[i].DestAir,Flight[i].Airline,Flight[i].Price,Flight[i].Duration,0,0,Flight[i].Price));
			break;
		}


	for(int i = 0; i<size; i++)
		for(int j = 0; j<size; j++)
			while (Origin == Flight[i].OriginAir && Dest ==  Flight[j].DestAir && Flight[i].DestAir == Flight[j].OriginAir){ 
				Temp3.push_back(Routes(Flight[i].OriginAir+">>"+Flight[i].DestAir,Flight[i].OriginAir,Flight[j].OriginAir," ",Flight[j].DestAir,
				Flight[i].Airline+" ---> "+Flight[j].Airline,
				Flight[i].Price+Flight[j].Price,Flight[i].Duration+Flight[j].Duration,0,0,0));
			break;
		}
	
	for(int i = 0; i<size; i++)
		for(int j = 0; j<size; j++)
			for(int k = 0; k<size; k++)
				while (Origin == Flight[i].OriginAir && Dest ==  Flight[k].DestAir 
					&& Flight[i].DestAir == Flight[j].OriginAir 
					&& Flight[j].DestAir == Flight[k].OriginAir 
					&& Flight[i].DestAir != Dest && Flight[j].DestAir != Dest && Flight[j].DestAir != Origin){
					Temp3.push_back(Routes(Flight[i].OriginAir+">>"+Flight[i].DestAir+">>"+Flight[k].OriginAir,Flight[i].OriginAir,
						Flight[j].OriginAir,Flight[k].OriginAir,Flight[k].DestAir,
						Flight[i].Airline+" ---> "+Flight[j].Airline+" ---> "+Flight[k].Airline,
						Flight[i].Price+Flight[j].Price+Flight[k].Price,
						Flight[i].Duration+Flight[j].Duration+Flight[k].Duration,0,0,0));
					break;
				}
/*After I have searched and stored all possible journey avaliable in vector<Routes> Temp3, the follow code will search through the airport data and 
add correct the departure tax, connection flight time and calculate the total flight time and total price for each journey.
Similar to before, i had multiple "for" loop to search through the airport data, finding the airport code that matches the Origin and Destination Airport code and
update the respective Departure Tax and connection flight time for each journey to the vector*/
	int size2 = Temp3.size();
	int size3 = Air.size();
	for(int n = 0; n<size2; n++)
		for(int m = 0; m<size3; m++)
			if (Temp3[n].Origin == Air[m].AirportCode){
					Temp3[n].DTax = Temp3[n].DTax+Air[m].DepartTax;
					Temp3[n].TPrice = Temp3[n].Cost+Temp3[n].DTax;
					for (int p = 0; p <size3; p++)
						if (Temp3[n].Con1 == Air[p].AirportCode){
							Temp3[n].DTax = Temp3[n].DTax+Air[p].DepartTax;
							Temp3[n].ConT = Temp3[n].ConT+Air[p].ConnectTime;
							Temp3[n].FlightDur = Temp3[n].FlightDur+Air[p].ConnectTime;
							Temp3[n].TPrice = Temp3[n].Cost+Temp3[n].DTax;	
							for (int q = 0; q <size3; q++)
								if (Temp3[n].Con2 == Air[q].AirportCode){
									Temp3[n].DTax = Temp3[n].DTax+Air[q].DepartTax;
									Temp3[n].ConT = Temp3[n].ConT+Air[q].ConnectTime;
									Temp3[n].FlightDur = Temp3[n].FlightDur+Air[q].ConnectTime;
									Temp3[n].TPrice = Temp3[n].Cost+Temp3[n].DTax;	
							}
						}
				}

	setSearchR(Temp3); // This will get a copy of the vector<Routes>Temp3 to the vector<Routes>SearchResults from above
}



void swap(int& a,  int& b) // A swap function needed to complete the bubblesort algorthm.
{
	int temp = a;
	a = b;
	b = temp;
}

void bubblesortC(vector<Routes>& v)  // A bubblesort Algorthm for Cost
{
	int size = v.size();
	for (int i=0; i<size-1; ++i)
		for (int j=0; j<size-1; ++j)
			if (v[j].TPrice>v[j+1].TPrice)
			{
				swap(v[j], v[j+1]);
			}
}

void bubblesortT(vector<Routes>& v) // A bubblesort Algorthm for Time
{
	int size = v.size();
	for (int i=0; i<size-1; ++i)
		for (int j=0; j<size-1; ++j)
			if (v[j].FlightDur>v[j+1].FlightDur)
			{
				swap(v[j], v[j+1]);
			}
}

void printresult(vector<Routes>& R,int i) // A function to print out the search result (e.g. all the records from vector<Routes> SearchResults)
{
		cout << left << "Flight Option "
		<< setw(20) << setfill('-') << i+1 << endl
		<< setw(9) << setfill(' ') << "Journey:"
		<< R[i].Journey
		<< right << setw(5) << setfill('>') << R[i].Destination << endl
		<< left << setw(11) << setfill(' ') << "ByAirline:"
		<< R[i].Airline << endl
		<< setw(13) << "TicketPrice:"
		<< setw(8) << R[i].Cost
		<< setw(14) << "DepartureTax:"
		<< setw(7) << R[i].DTax
		<< setw(12) << "TotalPrice:"
		<< setw(8) << R[i].TPrice
		<< setw(10) << "Duration:"
		<< R[i].FlightDur << endl;
		cout << endl;
	}

// A function to search all the Arrival and Departure flights based on the string and store them respective flight vectors.
void SearchAir(string Code){ 
	
	vector<Flights> Flight = getFlightR();
	vector<Flights> DepartFlight;
	vector<Flights> ArriFlight;
	
	int size = Flight.size();
	for(int i = 0; i<size; i++){
		while (Code == Flight[i].OriginAir){
			DepartFlight.push_back(Flight[i]);
			break;
		}
		while (Code ==  Flight[i].DestAir){
			ArriFlight.push_back(Flight[i]);
			break;
		}
	}
	setDepartFlig(DepartFlight); //Copy vector results to vector<Flights> DepartFlight at the start of the file.
	setArriFlig(ArriFlight); //Copy vector results to vector<Flights> ArriFlight at the start of the file.
}

/* A function which will search and display all the information about the inputed airport (from string acode), 
it will compare the string with all the element of Airport vector and output the right one.*/
void AirportInfo(string acode){ 
	vector<Airports>& Air = getAirportR();
	int size = Air.size();
	for (int i = 0; i<size; ++i){
	if(acode == Air[i].AirportCode){
		cout << endl;
		cout << left << setw(35) << setfill('-') << "Airport Information" << endl;
		cout << setw(14) << setfill(' ') << "Airport Code:";
		cout << setw(4) << Air[i].AirportCode << endl;
		cout << setw(14) << "Airport Name:";
		cout << setw(18) << Air[i].AirportName << endl;
		cout << setw(15) << "Departure Tax:";
		cout << setw(15) << Air[i].DepartTax;
		cout << setw(21) << "Min Connection Time:";
		cout << setw(5) << Air[i].ConnectTime << endl << endl;
	}
}
}
void DepArri(){ // A function which print out all the results from vector<Flights> ArriFlight and vector<Flights> DepartFlight
	vector<Flights> depflig = getDepartFlig();
	vector<Flights> Arriflig = getArriFlig();
	
	cout << "Flight - Departures" << endl;
		cout << setw(15) << setfill(' ') << "Journey";
		cout << setw(20) << "Airline";
		cout << setw(10) << "Price";
		cout << setw(10) << "Duration" << endl;
		cout << setw(53) << setfill('-') << "-" << endl;

	int size1 = depflig.size();
	for (int i = 0; i<size1; ++i){		
		cout << depflig[i].OriginAir << "-->";
		cout << setw(9) << setfill(' ') << depflig[i].DestAir;
		cout << setw(20) << depflig[i].Airline;
		cout << setw(10) << depflig[i].Price;
		cout << setw(10) << depflig[i].Duration << endl;
	}
	cout << endl;
		cout << "Flight - Arrivals" << endl;
		cout << setw(15) << setfill(' ') << "Journey";
		cout << setw(20) << "Airline";
		cout << setw(10) << "Price";
		cout << setw(10) << "Duration" << endl;
		cout << setw(53) << setfill('-') << "-" << endl;

	int size2 = Arriflig.size();
	for (int i = 0; i<size2; ++i){		
		cout << Arriflig[i].OriginAir << "-->";
		cout << setw(9) << setfill(' ') << Arriflig[i].DestAir;
		cout << setw(20) << Arriflig[i].Airline;
		cout << setw(10) << Arriflig[i].Price;
		cout << setw(10) << Arriflig[i].Duration << endl;
		}
	cout << endl;
}

void printReceipt(vector<Routes>& R, int i, Date IDate){	// A function which will print out the receipt of the booked flight
	cout << endl << right << setw(40) << setfill('*') << "Receipt" << left << setw(33) << '*' << endl << endl
			<< "Flight Information" << endl << endl
			<< left << setw(9) << setfill(' ') << "Journey:"
			<< R[i].Journey
			<< right << setw(5) << setfill('>') << R[i].Destination
			<< setw(30) << setfill(' ') << "Date of Flight: "
			<< left << IDate << endl
			<< setw(18) << setfill(' ') << "With Airline(s):" << endl
			<< setw(48) << R[i].Airline
			<< endl << endl 
			<< setw(22) << "FlightDuration:" 
			<< setw(10) << R[i].FlightDur-R[i].ConT 
			<< setw(14) << "TicketPrice:"
			<< setw(8) << R[i].Cost << endl
			<< setw(22) << "FlightConnectionTime:"
			<< setw(10) << R[i].ConT
			<< setw(14) << "DepartureTax:"
			<< setw(7) << R[i].DTax << endl 
			<< setw(54) << setfill('-') << "-" << endl
			<< setw(22) << setfill(' ') << "TotalDuration:"
			<< setw(10) << R[i].FlightDur 
			<< setw(14) << setfill(' ') << "TotalPrice:  "
			<< setw(8) << R[i].TPrice << endl
			<< endl;
}

// A function which check whether the entered AirportCode is valid and existed in the system
void checkCode(string a){ 
	vector<Airports>Code = getAirportR();
	vector<string>temp;
	if (a.size() != 3){
		throw runtime_error("Invalid Airport Code: Airport Code should only have 3 characters");
	}
	int size = Code.size();
	for (int i=0; i<size; ++i){
		if (Code[i].AirportCode == a){
			temp.push_back(Code[i].AirportCode);
		}
	}
	if (temp.size() == 0){
		throw runtime_error("Invalid Airport Code: Airport Code doesn't exist");
	}

}

// A function that output all the Airport Codes and Airport Names from vector<Airports> AirportRecords (Airport data)
void DisplayCode(){
	vector<Airports>Code = getAirportR();
	cout << left << setw(15) << setfill(' ') <<"Airport Code";
	cout << left << setw(20) << "Airport Name" << endl;
	cout << setw(50) << setfill('-') << "-" << endl;
	int size = Code.size();
	for (int i = 0; i<size; ++i){
		cout << left << setw(15) << setfill(' ') << Code[i].AirportCode;
		cout << left << setw(20) << Code[i].AirportName << endl;
	}
	throw 1;
}
