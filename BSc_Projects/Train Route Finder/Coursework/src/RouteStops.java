/* This class exists to provide the functionality of the Routes (Finding stops between stations). */
import java.io.*;
import java.util.*;
import javax.swing.*;


public class RouteStops {
    private ArrayList<String>[][] routestops;
    private String [] Station;
    private int stat1,stat2;
    private String Origin, Dest;

    public RouteStops() {
        RoutesData data = new RoutesData();
        DataIO data2 = new DataIO();
        Station = data.getstation();
        routestops = data2.getstops();
            
        Scanner scanner = new Scanner(System.in);
       
        while(true){ //If error is thrown, it will repeat this part of the program until it reach break;
         try{
            System.out.print("Please enter the station you like to depart from: ");
            this.Origin = scanner.next();
            if (checkstat(Origin)){ //check if String is a valid station in the system
                throw new Exception("Invalid Station: Station doesn't exist in the database");
            }
            break;} //break out the while loop
        catch (Exception e) { //Throw error if input is not a valid station
            System.out.println("Error: " + e.getMessage());
        } }
        while(true){
         try{
            System.out.print("Please enter the station you like to arrive to: ");
            this.Dest = scanner.next();
            if (checkstat(Dest)){
               throw new Exception("Invalid Station: Station doesn't exist in the database");
            }
            if (Dest.equals(Origin)){
                throw new Exception("Inputted Stations are identical, Please enter another station");
            }
            break;  }
       catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }  }  
 
        stat1 = searchstat(Origin); //Search for the integer position of station in the system(in the Station array - look at RoutesData)
        stat2 = searchstat(Dest);
        if (routestops[stat1][stat2].size() == 0){ //Finding out if there are any stops between these station
            System.out.println("There are no stop between these stations");
        }
        else{
        System.out.println("There are the list of stops between these two stations ");
        for (int i=0; i<routestops[stat1][stat2].size(); i++) { //Outputing the stops to screen
            if (i+2 > routestops[stat1][stat2].size()){ 
                System.out.printf("%s\n",routestops[stat1][stat2].get(i));
            }
            else{
                System.out.printf("%s%s",routestops[stat1][stat2].get(i)," --> ");
            }
        }
        }
        gomenu();
    }
    private int searchstat(String st){ //Function to search the position of the station in the array
         int t =0;
         for (int i=0; i<Station.length; i++){
              if(Station[i].equals(st)){
                   t = i;
              break;
              }}
        return t;
        }
   
    public void gomenu() //Function to return to MainInterface
    {
        try {
            System.out.println();
            System.out.println("Returning to Main menu...");
            String[] args = { };
            MainInterface.main(args);
        } catch (IOException e) {
            System.out.println("Cannot find default file");
        }
}

 private boolean checkstat(String st){ //Function to check whether the station inputted is a valid station in the system
        boolean C = true;
          for (int i=0; i< Station.length; i++){
            if (Station[i].equals(st)){   
                C = false;
            } }
          return C;
     }
}
