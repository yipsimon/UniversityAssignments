/*
The date class is necessary to work for the Price functionality, to determine 
whether the date that the user has inputted is entitled to the discount scheme 
if the date is the last day of the month. 
*/
public class Date {
    private int day, month, year;
    private String[ ] monthName = { "January", "February", "March", 
                            "April", "May", "June", "July",
                            "August", "September", "October",
                            "November", "December" }; //array contain the months in words
    public String getDate(){ //getting the date
        return day+" "+monthName[month-1]+" "+year;
    }
    
    public void setDate(int d, int m, int y){ //Setting the date as date class object
         day = d;
         month = m;
         year = y;
    }
    
    public int day(){ //getting the day
	return day;
    }

    public int month(){ //getting the month
	return month;
    }

    public int year(){ //getting the year
	return year;
    }

    public int daysinmonth(int y, int m){ //workign the days in month
	switch (m) {
            case 2:
		return (leapyear(y))?29:28; // the length of February varies
	    case 4: case 6: case 9: case 11:
		return 30;
	    default:
		return 31;
		}
        }

    public static boolean leapyear(int y) { //working out the leapyear for february 
        boolean leap = false;
	if (y%4!=0){
			leap = false;}
        else if (y%100==0 && y%400!=0){
			leap = false;}
        else{ 
            leap = true;}
        return leap;
    }
    
    public boolean lastdaymonth(int d, int m, int y){ //working whether the date is the last day of the month
        boolean last = false;
        if (d == daysinmonth(y,m)){
            last = true;}
        return last;
    }
}
