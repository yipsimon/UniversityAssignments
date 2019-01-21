/* Main Menu with switch function which will go to other parts of the program*/

import java.io.*;
import java.util.*;
import javax.swing.*;
import java.io.FileNotFoundException;

public class MainInterface {
   public static void main(String[] args) throws FileNotFoundException, IOException{
       
       Scanner scanner = new Scanner(System.in);
       
       System.out.println("Welcome to Train Route Finder Program");
       System.out.println("Please enter the function you would like");
       System.out.printf("%d%s%d%s%d%s\n%d%s%d%s\n%d%s%d%s\n",
               1, ". Time    ", 2, ". Price    ", 3, ". Route", 4, ". Split Ticket  ", 5, ". Sort Routes",
               6, ". Admin Menu    ",7,". Exit Program");
       try{
       int menuChoice = scanner.nextInt();
       
           switch (menuChoice) {
            case 1: //Entering integer 1 will run Time() in CalcDat class
                CalcData sel = new CalcData();
                sel.Time();
                break;
            case 2: //Entering integer 2 will run Price() in CalcDat class
                CalcData sel2 = new CalcData();
                sel2.Price();
                break;
            case 3: //Entering integer 1 will run RouteStops() in RouteStops class
                RouteStops sel3 = new RouteStops();
                break;
            case 4: //Entering integer 4 will run SplitTicket() in CalcDat class
                CalcData sel4 = new CalcData();
                sel4.SplitTicket();
                break;
            case 5: //Entering integer 5 will run SortRoutes() in SortRoutes class
                SortRoutes sel5 = new SortRoutes();
                break;
            case 6: //Entering integer 6 will run menu() in Admin class
                Admin sel6 = new Admin();
                sel6.menu();
                break;
            case 7: //break and end program
                System.out.println("Terminate program");
                break;
            default: //Output error message and end program
                System.out.println("Did not select a function");
                System.out.println("Terminate program");
            break;
           }
       }
       catch (InputMismatchException e){ //catch exception if inputted value is not an integer
           System.out.println("Did not select a function");
           System.out.println("Terminate program");
        }
}
}


 

