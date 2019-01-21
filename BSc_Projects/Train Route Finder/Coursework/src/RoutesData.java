/*
RoutesData class contains fixed data provided in the specification such as the 
Station’s names, their prices and durations.
 */
import java.util.*;

public class RoutesData {
       //private int time;
       //private double prices;
       
       private String[] stations = {"Leicester", "Loughborough", "Nottingham", "Derby", "York"}; //Array to store all stations
       
       private double [][] prices = { {0, 2.50, 3.50, 13.00 ,23.50}, {2.50, 0, 1.50, 2.25, 11.50}, //2D Array to store all the prices of the stations
                               {3.50, 1.50, 0, 2.50, 11.50}, {13.70, 2.00, 2.50, 0, 11.20},
                                    {22.20, 12.00, 11.20, 11.20}};       
       private int [][] durations = { {0, 10, 30, 48, 65}, {10, 0, 15, 23, 60}, {30, 15, 0, 12, 40}, //2D Array to store all the time of the stations
                                {48, 25, 10, 0, 45}, {70, 60, 40, 45, 0}};
       
       public String[] getstation(){ //function for using the station array in another class
           return stations; 
       }
       public double [][] getprices(){ //function for using the price array in another class
           return prices;
       }
       public int [][] gettime(){ //function for using the duration array in another class
           return durations;
       }
      
       
}
