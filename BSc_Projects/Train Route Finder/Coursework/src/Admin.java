/*
 Admin Menu, containing the functionality of inputing, saving and retrieving routes
 */

import java.io.*;
import java.util.*;
import javax.swing.JFileChooser;
import javax.swing.filechooser.FileNameExtensionFilter;

public class Admin {
    private ArrayList<String>[][] routestops;
    private ArrayList<String> inputstops = new ArrayList<String>();
    private ArrayList<String> updatedstat = new ArrayList<String>();
    private String [] Station;
    private String Origin,Dest;
    
    public Admin(){
        RoutesData data = new RoutesData();
        DataIO data2 = new DataIO();
        Station = data.getstation();
        routestops = data2.getstops();
    }

    public void menu(){ //Choosing which functionality the user want by using the switch statement
        System.out.println("Welcome to Admin menu");
        System.out.println("Here you can add, save and import routes from other files \nPlease select the function you would like");
        System.out.printf("%d%s%d%s%d%s\n%d%s\n",
               1, ". Input Route    ", 2, ". Save Route    ", 3, ". Retrieve Route", 4, ". Return to Main Menu");
        try{
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        switch (n) {
            case 1:
                Input(); //Go to input function
                break;
            case 2:
                save(); //Go to input function
                break;
            case 3:
                retrieve(); //Go to input function
                break;
            case 4:
                gomenu(); //Return to Main Menu
                break;
            default:
                System.out.println("Did not select a function");
                gomenu(); //Return to Main Menu
        }
    }
    catch (InputMismatchException e){
           System.out.println("Did not select a function");
           gomenu(); //Return to Main Menu
        }
    }

    public void Input(){ //Input Route functionality
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
                throw new Exception("Inputted Stations are identical, Please enter another stop");
            }
            break;  }
        catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }  }  
        
        System.out.println("Please input the stops between these stations (Enter Exit to terminate input)");
        while(true){ //Continue looping until it reaches break;
            try{
                String stop = scanner.next();
                if(stop.equals(Origin)||stop.equals(Dest) ){ //Checking if stop entered is the same as the Origin and Destination station, throw error if it does.
                    throw new Exception("Inputted stop is identical to Departure or Arrival Staion \nPlease enter another stop");
                }
                if(stop.equals("Exit")){ //Continue adding stops until Exit is entered
                    break;
                }
                inputstops.add(stop); //Add stop to inputstops array
            }
            catch (Exception e){
                System.out.println("Error: " + e.getMessage());
            }
        }
        int stat1 = searchstat(Origin); //Search for the integer position of station in the system(in the Station array - look at RoutesData)
        int stat2 = searchstat(Dest);
        while (!routestops[stat1][stat2].isEmpty()){ //if there exist stops between these station, this while loop will delete these stops completely
            int i = 0;
            routestops[stat1][stat2].remove(i);
        }
        for (int j = 0; j < inputstops.size(); ++j){ //Adding the inputted stop into the routestops array
            routestops[stat1][stat2].add(j,inputstops.get(j));
        }

        System.out.printf("\n%s\n%s\n\n","Please note that the inputted stops will need to be saved "
                ,"by option 2 in Admin menu otherwise it will be delete upon program exit.");
        System.out.println("Returning to Admin menu...");
        menu(); //Return to Admin menu
    }

    public void save(){ //Save Route functionality
        System.out.println("This is the save process which will save all the info on journey stops");
        System.out.println("Would you like to save the info into");
        System.out.println("1) A Default data file      2) A new route information file");
        Scanner scanner = new Scanner(System.in);
        int input = scanner.nextInt();
        switch (input) {
            case 1: //Saving as default data file
                try{
                File outdFile = new File("Routes.txt"); //Finding the default file "Routes.txt" or creating it, if it doesn't exist
                PrintWriter out = new PrintWriter(outdFile); //create PrintWriter object and open file
                for (int i = 0; i<5; ++i){
                    for(int j = 0; j<5; ++j){
                    if(!routestops[i][j].isEmpty()){
                        out.printf("%s%-10s%-10s","Route ",Station[i],Station[j]); // write to the stream (i.e. to file)
                        out.println();
                        for(int k=0; k<routestops[i][j].size(); ++k){ //loop to write the stops
                            if(k == routestops[i][j].size()-1){ //if it is the last stop
                                out.println(routestops[i][j].get(k)); //writing the last stop (without ",")
                                out.println();
                                break; //break out of writing the stops for that route
                            }
                            out.print(routestops[i][j].get(k)+","); // writing the stops
                        }
                    }    
                    }
                }
                out.close(); // output done, so close the stream
                System.out.println("Data has been saved into the default route file");
                System.out.println("Returning to Admin menu...");
                System.out.println();
                menu(); //return to Admin menu
                break;
                }
            catch (FileNotFoundException e){
                System.out.println("Cannot find default Routes file, \nPlease use Option 2 under the save section to save data");
                System.out.println("Returning to Admin menu...");
                System.out.println();
                menu();
            }
            case 2: //Saving as new data file
                try{
                File workingDirectory = new File(System.getProperty("user.dir")); 
                JFileChooser chooser=new JFileChooser(workingDirectory);
                FileNameExtensionFilter filter = new FileNameExtensionFilter("Text File", "txt"); 
                chooser.setFileFilter(filter);
                chooser.showSaveDialog(null);   // save dialog box
                File outFile = chooser.getSelectedFile();
                if (outFile.equals(null)){
                    throw new NullPointerException();
                }
                PrintWriter out1 = new PrintWriter(outFile+".txt"); //save as a text file
                
                for (int i = 0; i<5; ++i){ //same as above, writing data to file
                    for(int j = 0; j<5; ++j){
                    if(!routestops[i][j].isEmpty()){
                        out1.printf("%s%-10s%-10s","Route ",Station[i],Station[j]);
                        out1.println();
                        for(int k=0; k<routestops[i][j].size(); ++k){
                            if(k == routestops[i][j].size()-1){
                                out1.println(routestops[i][j].get(k));
                                out1.println();
                                break;
                            }
                            out1.print(routestops[i][j].get(k)+",");
                        }
                    }    
                    }
                }
                out1.close();
                System.out.println("Data has been saved into a new route file");
                System.out.println("Returning to Admin menu...");
                System.out.println();
                menu();
                }
                catch (FileNotFoundException e){
                    System.out.println("Cannot find file");
                    System.out.println("Returning to Admin menu...");
                    System.out.println();
                    menu();
                }
                catch (NullPointerException e){ //if user click cancel in the dialog box, it will return this error
                    System.out.println("Save operation has been cancelled");
                    System.out.println("Returning to Admin menu...");
                    System.out.println();
                    menu();
                }
                break;
            default:
                System.out.println("Please select one of the options");
                System.out.println("Returning to Admin menu...");
                System.out.println();
                menu();
                break;
        }
        
    }

    public void retrieve(){ //Retrieve Route functionality
        System.out.println("Please select a file to import new stops data");
        try{
        File workingDirectory = new File(System.getProperty("user.dir"));
        JFileChooser chooser = new JFileChooser(workingDirectory);
        chooser.showOpenDialog(null); // open dialog box
        File inFile=chooser.getSelectedFile();
        if (inFile.equals(null)){
                    throw new NullPointerException();
        }
        Scanner in = new Scanner(inFile);
        
        RoutesData data = new RoutesData();
        Station = data.getstation();
      
        String Indicator = in.next();
        String Station1 = in.next();
        String Station2 = in.next();
        String line,stop;
        
        for (int i=0; i<5; i++) { //this is similar to the DataIO, for reading stops in the system with a few differences
            for (int j=0; j<5; j++) {
            if (Indicator.equals("Route") && Station1.equals(Station[i])
                && Station2.equals(Station[j])){
                    updatedstat.add(Station[i]);
                    updatedstat.add(Station[j]);
                    line = in.next();
                    stop = line.substring(0, line.indexOf(',')); 
                    while (!routestops[i][j].isEmpty()){ //If there already exist stops between the stations being importted, if will delete these stops
                            int k = 0;
                            routestops[i][j].remove(k);
                    }
                    while(line.length() != 0){
                        routestops[i][j].add(stop);
                        line = line.substring(line.indexOf(',')+1);
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
                        }}}}}
        in.close();
        System.out.println("The imported data is updated or overwriten to the system"); 
        System.out.println("The updated routes are:");
        System.out.printf("%-15s%-15s\n","From","To");
        for (int i = 0; i < updatedstat.size(); ++i){ //Displaying all the station that has been updated
            System.out.printf("%-15s%-15s\n",updatedstat.get(i),updatedstat.get(i+1));
            i = i+1;
        } 
        System.out.println("Returning to Admin menu...");
        System.out.println();
        menu(); //Return to Main Menu
        }
        catch (FileNotFoundException e){
                    System.out.println("Cannot find file specified");
                    System.out.println("Returning to Admin menu...");
                    System.out.println();
                    menu();
                }
        catch (NullPointerException e){ //if user click cancel in the dialog box, it will return this error
                    System.out.println("Importing route data operation has been cancelled");
                    System.out.println("Returning to Admin menu...");
                    System.out.println();
                    menu();
        }
        catch (NoSuchElementException e){ //if the program cannot read data, it will return this error
            System.out.println("Error reading the data from file, data are missing or corrupted");
            System.out.println("Unable to recover from error, End Program");
            System.exit(0); 
        }
    }
    
    private int searchstat(String st){ //Function to search the position of the station in the array
         int t =0;
         for (int i=0; i<Station.length; i++){
              if(Station[i].equals(st)){
                   t = i;
              break;
              }
        }
        return t;
        }
    
    public void gomenu() //Function to return to MainInterface
    {
        try {
            System.out.println();
            System.out.println("Returning to Main menu...");
            String[] args = { };
            MainInterface.main(args);
        } 
        catch (IOException e) {
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

