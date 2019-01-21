/*
This class is necessary for the SortRoutes functionality. It is necessary 
because I need to create constructor define the structure of the data in this 
order “Origin Station, Destination, Price, Time and NumofStops” in order to 
create an arraylist which has this structure so I can display the sort in a 
table format. 
 */

public class RouteCon {
    private String station1, station2;
    private double prices;
    private int time,numofstops;

    RouteCon(String station1, String station2, double prices, int time,int numofstops) { //default constructor
        this.station1 = station1;
        this.station2 = station2;
        this.prices = prices;
        this.time = time;
        this.numofstops = numofstops;
    }
       public String getstat1(){ //getting the first station
           return station1;
       }
       public String getstat2(){ //getting the second station
           return station2;
       }
       public int gettime(){ //getting the time
           return time;
       }
       public double getprice(){ //getting the price
           return prices;
       }
       public int getstops(){ //getting the number of stops
           return numofstops;
       }
}
