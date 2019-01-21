/*
The purpose of DataIO.java class is to import routes (stops) data from default 
files and store the data within the system, in the ArrayList. 
A function is also created to use the arraylist in other classes. 
 */

import java.io.*;
import java.util.*;

public class DataIO {
    private ArrayList<String>[][] routestops = new ArrayList[5][5]; //2D Arraylist to store stops
    private String [] Station;
    public DataIO(){
        try {
            File inFile = new File("Routes.txt"); //Read the default file named "Routes.txt"
            RoutesData data = new RoutesData();
            Station = data.getstation();
            for (int i=0; i<5; i++) {
                for(int j=0; j<5; j++) {
                    routestops[i][j]= new ArrayList<String>(); //Making each element of the routestops Arraylist contain a arraylist within.
                }}
            Scanner in = new Scanner(inFile);
            String Indicator = in.next();
            String Station1 = in.next();
            String Station2 = in.next();
            String line,stop;
            int k = 0;
            for (int i=0; i<5; i++) {
                for (int j=0; j<5; j++) {
                    if (Indicator.equals("Route") && Station1.equals(Station[i]) //If the format of the data in the file matches with this, it will read the data as store it in the arraylist
                            && Station2.equals(Station[j])){
                        k = k + 1; //an indicator showing how many routes it has imported
                        line = in.next();
                        while(line.length() != 0){
                            if(!line.contains(",")){
                                stop = line;
                                routestops[i][j].add(stop);
                                if(in.hasNext()){
                                    Indicator = in.next();
                                    Station1 = in.next();
                                    Station2 = in.next();}
                                break;
                            }
                            else{
                                stop = line.substring(0, line.indexOf(','));
                                routestops[i][j].add(stop);
                                line = line.substring(line.indexOf(',')+1);
                            }}}}}
            in.close();
            if(k == 0){ //if not route is imported this mean there is something wrong with the file, throw this error
                throw new NoSuchElementException ();
            }
        } catch (FileNotFoundException e) { //Error for is file is not found
            System.out.println("Cannot find default Routes file");
        }
        catch (NoSuchElementException e){
            System.out.println("Error reading the data from the Routes file, data are missing or corrupted");
            System.out.println("Unable to recover from error, End Program");
            System.exit(0);  //Program will terminate
        }
    }
    
    public ArrayList<String>[][] getstops(){ //Getting the routestops arraylist for other classes to use
           return routestops;
       }
}
