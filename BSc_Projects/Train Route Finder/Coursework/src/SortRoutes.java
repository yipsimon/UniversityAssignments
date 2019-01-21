/* This class exists to provide the functionality of the sorting the routes in the system. */
import java.io.IOException;
import java.util.*;

public class SortRoutes {
        private String [] Station;
        private double [][] Price;
        private int [][] Duration;
        private List<RouteCon> trainRoutes = new ArrayList<RouteCon>();
        private ArrayList<String>[][] stops;
        private int num;
        
    public SortRoutes(){
        
            System.out.println("There are the list of all Routes in this system: ");
            System.out.printf("%-15s%-15s%-15s%-10s%-15s\n","From","To","Price",
                    "Time","No. of stops en route"); //Printing out the column names
            RoutesData data = new RoutesData(); //Getting data from RoutesData
            DataIO data2 = new DataIO();  //Getting data from DataIO
            Station = data.getstation();
            Price = data.getprices();
            Duration = data.gettime();
            stops = data2.getstops();
            
        for (int i=0; i<Station.length; i++){   //Compiling all the data together into an arraylist - trainRoutes
            for (int j=0; j<Station.length; j++){
                if(i != j){
                    String Station1 = Station[i];
                    String Station2 = Station[j];
                    double prices = Price[i][j];
                    int time = Duration[i][j];
                    int numofstops = stops[i][j].size();
                    trainRoutes.add(new RouteCon(Station1, Station2, prices, time,numofstops));  
                    System.out.printf("%-15s%-15s%-15.2f%-10d%-10d\n",
                            Station[i],Station[j],Price[i][j],Duration[i][j],stops[i][j].size());
                    }
                }
            }
        System.out.println("Sort Routes by 1.price, 2.time or 3.number of stops en route:");
        while(true){
            try{
                Scanner scanner = new Scanner(System.in);
                num = scanner.nextInt();
                break;
            }
            catch(InputMismatchException e){
                System.out.println("Error: Input is not an integer, Please enter an integer");
            } 
        }
            
            switch (num) { 
            case 1: 
                bubblesortC();
                System.out.println("Sorted by Price:");
                System.out.printf("%-15s%-15s%-15s%-10s%-15s\n","From","To","Price",
                    "Time","No. of stops en route");
                break;
            case 2:
                bubblesortT();
                System.out.println("Sorted by Time:");
                System.out.printf("%-15s%-15s%-15s%-10s%-15s\n","From","To","Price",
                    "Time","No. of stops en route");
                break;
            case 3:
                bubblesortR();
                System.out.println("Sorted by No. of stops:");
                System.out.printf("%-15s%-15s%-15s%-10s%-15s\n","From","To","Price",
                    "Time","No. of stops en route");
                break;
            default:
                System.out.println("Didn't enter a sort");
                gomenu();} // Return to main menu
                
            for (int i=0; i<trainRoutes.size(); i++){ //Printing out the data in the trainRoutes arraylsit
              System.out.printf("%-15s%-15s%-15.2f%-10d%-10d\n",
                      trainRoutes.get(i).getstat1(),trainRoutes.get(i).getstat2(),
                      trainRoutes.get(i).getprice(),trainRoutes.get(i).gettime(),
                      trainRoutes.get(i).getstops());
            }
            gomenu();
            }

public void bubblesortC()  // A bubblesort Algorthm for Price
{
	int size = trainRoutes.size();
	for (int i=0; i<size-1; ++i)
		for (int j=0; j<size-1; ++j)
			if (trainRoutes.get(j).getprice()>trainRoutes.get(j+1).getprice())
			{
				swap(j,j+1);
			}
}

public void bubblesortT()  // A bubblesort Algorthm for Time
{
	int size = trainRoutes.size();
	for (int i=0; i<size-1; ++i)
		for (int j=0; j<size-1; ++j)
			if (trainRoutes.get(j).gettime()>trainRoutes.get(j+1).gettime())
			{
				swap(j,j+1);
			}
}

public void bubblesortR()  // A bubblesort Algorthm for Stops
{
	int size = trainRoutes.size();
	for (int i=0; i<size-1; ++i)
		for (int j=0; j<size-1; ++j)
			if (trainRoutes.get(j).getstops()>trainRoutes.get(j+1).getstops())
			{
				swap(j,j+1);
			}
}

private void swap(int a,int b) // A swap function needed to complete the bubblesort algorthm.
{
    List<RouteCon> temp = new ArrayList<RouteCon>();
        temp.add(trainRoutes.get(a));
	trainRoutes.set(a, trainRoutes.get(b));
	trainRoutes.set(b, temp.get(0));
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
}
