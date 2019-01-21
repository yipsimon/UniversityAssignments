#include "std_lib_facilities.h"
#include "DataIO.h"
#include "Routes.h"
#include "Flights.h"
#include "Airports.h"
#include "DataConfig.h"

void ImportData(){
	ImportAirport();
	ImportFlights();
}

void ImportAirport(){
	vector<Airports> Temp;	//Temporary class Airports vector to store the information from files

	ifstream fileIn("airports.txt");
	
	if(!fileIn){		//If the program cannot find the file, throw the error
		throw exception("Can't open airports.txt file");
	}

	string Code;
	string Name;
	int DeptTax;
	int ConnectTime;

	while (!fileIn.eof() ){
		fileIn >> Code >> Name >> DeptTax >> ConnectTime;
		if (Code.size() != 3 || DeptTax < 0 || ConnectTime < 0){
		throw exception("Incorrect Information in file! Check airports.txt file");
		}
		Temp.push_back( Airports(Code, Name, DeptTax, ConnectTime ) );
		if (fileIn.fail()){
			throw exception("File Corrupted! check airports.txt file");
			break;
		}

	}

	setAirportR(Temp); //Copying the information from Temp to vector<Airports>AirportRecords
}

void ImportFlights(){
	vector<Flights> Temp2; //Temporary class Flights vector to store the information from files

	ifstream fileIn("flights.txt");

	if(!fileIn){		//If the program cannot find the file, throw the error
		throw exception("Can't open flights.txt file");
	}


	string Origin;
	string Destination;
	string Line;
	int Price;
	int Duration;

	while (!fileIn.eof() ){
		fileIn >> Origin >> Destination >> Line >> Price >> Duration;
		if (Origin.size() != 3 || Destination.size() != 3 || Price < 0 || Duration < 0){
		throw exception("Incorrect Information in file! Check flights.txt file");
		}
		Temp2.push_back( Flights( Origin, Destination, Line, Price, Duration ) );
		if (fileIn.fail()){
			throw exception("File Corrupted! check flights.txt file");
			break;
		}
	}

	setFlightR(Temp2); //Copying the information from Temp2 to vector<Flights>FlightRecords
}


void ExportData(vector<Routes>& R, int C, Date DateofFlight){ //This function will export a receipt for the booking information

	ofstream fileOut("Receipt.txt"); //Write to "Receipt.txt" or Create and write to "Receipt.txt" if file doesn't exist
	if (!fileOut)
	error("canÅft open output file Receipt.txt");
	int i=C;
		fileOut << endl << right << setw(40) << setfill('*') << "Receipt" << left << setw(33) << '*' << endl << endl
			<< "Flight Information" << endl << endl
			<< left << setw(9) << setfill(' ') << "Journey:"
			<< R[i].Journey
			<< right << setw(5) << setfill('>') << R[i].Destination
			<< setw(28) << setfill(' ') << "Date of Flight: "
			<< left << DateofFlight << endl
			<< left << setw(18) << setfill(' ') << "With Airline(s):" << endl
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
			<< endl
			<< "Thank you booking a flight with us, " << endl;

	fileOut.close(); // close file
	
}