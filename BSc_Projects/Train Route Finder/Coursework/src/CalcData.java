/* This class exist to provide the functionality of Price, Time and SplitTicket in the program. */

import java.io.*;
import java.util.*;

public class CalcData {
    private String [] Station;
    private int [][] Duration;
    private double [][] Price;
    private int stat1, stat2, stat3, ctime, htime, mtime;        
    private double Tprice, Dprice, Cprice;
    private String Origin, Dest;
    private Date inputdate = new Date();
        
   public CalcData(){
        RoutesData data = new RoutesData(); //Getting the RoutesData Class and linking them to array above
        Station = data.getstation();
        Duration = data.gettime();
        Price = data.getprices();

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
        }  }  }
    
    public void Time(){ //Time functionality
        stat1 = searchstat(Origin); //Search for the integer position of station in the system(in the Station array - look at RoutesData)
        stat2 = searchstat(Dest);
        ctime = Duration[stat1][stat2];  //Get the Time from the Duration 2d array using the integer we have just found.
        htime = ctime/60;   //working out the hours
        mtime = ctime%60;   //working out the minutes
           
        System.out.printf("\n%s%s%s%s%s\n%s%d%s%d%s\n",
                           "From ", Origin, " Station to ", Dest, " Station",
                           "Total Time of Travel = ", htime, " hours ", mtime, " minute");   
        gomenu(); //Return to menu
        }
        
    public void Price(){ //Price functionality 
      while (true){
      try{
         Scanner scanner = new Scanner(System.in);
         System.out.print("Please enter date in dd mm yyyy format: (With spaces)");
         int day = scanner.nextInt();
         int month =scanner.nextInt();
         int year = scanner.nextInt();
         inputdate.setDate(day,month,year); //Storing the integers into the date object
         if (day <= 0 || day > inputdate.daysinmonth(year, month) //Checking if it is a valid date
                || month <=0 || month > 12|| year < 2015 || year > 2030){
             throw new Exception("Invalid date: Please enter a valid date"); 
            }
            break; }
      catch(InputMismatchException e){ //Catching anything that is not an integer input
          System.out.println("Error: Input is not integers or incorrect format");
      } 
      catch (Exception e) { //Catching the Exception
          System.out.println("Error: " + e.getMessage());
      }
      }       
            stat1 = searchstat(Origin);
            stat2 = searchstat(Dest);
            Tprice = Price[stat1][stat2]; //Total Price
   
            if(inputdate.lastdaymonth(inputdate.day(), inputdate.month(), inputdate.year())){ //If is it the last day of the month. discount is applied to the total price
                Tprice = Tprice*0.9;
                System.out.print("\n**As you are traveling on the last day of the month, "
                        + "\nby our discount scheme, your fare will be reduced by 10% \n");
            }
            System.out.print("Date: "+inputdate.getDate());
            System.out.printf("\n%s%s%s%s%s\n%s%.2f\n",
                   "From ", Origin, " Station to ", Dest, " Station",
                   "Total Price of ticket: £", Tprice);   
            gomenu();   //Return to menu
            }
      
        public void SplitTicket(){
            
            stat1 = searchstat(Origin);
            stat2 = searchstat(Dest);

            Dprice = Price[stat1][stat2];
            Cprice = Dprice;

            for (int i=0; i<Station.length; i++){
                if(i!=stat1 && i!=stat2 && (Price[stat1][i]+Price[i][stat2] < Price[stat1][stat2])){ //Checking if there is a cheaper journey
                    if(Cprice> Price[stat1][i]+Price[i][stat2] ){ //Checking if it is cheaper than the previous one we have found
                        stat3 = i; //stat3 is fill with the position of the station of the array
                        Cprice = Price[stat1][stat3]+Price[stat3][stat2];
                        }
                    }
                }

            if (stat3 != stat1 && stat3 != stat2){ //if stat3 is not the same as the inputted station that cheap indirect routes exists
                System.out.println("Indirect journeys are cheaper compare to direct journey");
            System.out.printf("%s%s%s%s%s%s\n%s%.2f\n","Journey: ",Origin," ---> ",Station[stat3]," ---> ",Dest,
                    "Ticket Price: £",Cprice);
            }
            else {
            System.out.println("Direct tickets are the cheapest price available to this Journey");
            System.out.printf("%s%s%s%s\n%s%.2f\n","Journey: ",Origin," ---> ",Dest,
                    "Ticket Price: £",Dprice);
            }
            gomenu(); //return to menu
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
     
     private boolean checkstat(String st){ //Function to check whether the station inputted is a valid station in the system
        boolean C = true;
          for (int i=0; i< Station.length; i++){
            if (Station[i].equals(st)){   
                C = false;
            } }
          return C;
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
}
