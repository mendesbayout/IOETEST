<h1>Overview</h1>
The solution uses a class for managing payments and other employees. 
Each instance of the employee class has hours worked, name, and credit information.
A data management class manages log files and, using information from its global variables
and from each employee's shift variables, calculates everyone's pay.


<h1>Architecture</h1>

Class - Class description

    V: Global Variable - Description
    A: Attribute - Description
    M: Method(inputs) - Method description

Payment - Class to calculate and manage payments for all employees

    V: RATES - A dictionary of dictionaries, with rates for each shift for weekdays and weekends
    V: WEEKDAYS - A tuple containing the abbreviations of all weekdays
    V: SHIFT_RANGE - A dictionary of tuples containing two time objects, with starting and ending times for each shift
    M: load_employees_shifts(path) - Method to read from the log file path and return it as a set of instances of the Employee class
    M: calculate_compensation(day, shift) - Method to calculate and return the compensation depending on the day and shift inputted
    M: update_credit(employees) - Method to update each employee's credit, by calling calculate_compensation to all elements of an inputted set of employees.
    M: slice_shift(shift) - Method to convert employee's working hours into hours per shift, returning it as a dictionary

Employee(name, shift_data) - Class to store information and instances for each employee

    A: name - Employee's name - string
    A: shift_data - Employee's shift already converted using method parse_shift - defaultdict
    A: credit - Employee's credit - float
    M: parse_shift(shift_data) - Method to convert shift data from the log file into a defaultdict with all worked hours, in each shift, in each day

<h1>Methodology</h1>

In the order each method is called:

    load_shifts reads from the log file, line by line, creating a new employee instance for each line. 
    It just splits by the "=" and uses the left element as the name input, and right element as the shift input
    of the employee class.
    
    parse_shift is used during initialization of an employee instance and it splits the shift string by the "," and then,
    for each element, it takes the first two characters to identify the day and the remaining is splitted by the "-" to
    get starting and ending working hours. Working hours are then converted to datetime objects. parse_shift returns a 
    defaultidict with days as keys and a tuple (start, end) hours as values.

    At this point, we have a set of employees.
    
    update_credit calls the calculate_compensation method for each shift in each day for each employee on the inputted set, and updates their credit attribute.
    
    CALCULATE checks if the inputted day is a weekday or weekend and then, by calling the slice_shift method, it can iterate through all shifts worked on that day and calculate the correct compensation
    
    slice_shift takes starting and ending hours in a day, and then returns how much hours have been worked in each separated shift.
    
    At this point, all employees credit are up to date.

Then, all employees' credits are printed together with their name, as follows: The amount to pay NAME is: CREDIT USD

<h1>Instructions</h1> 

    In order to run the solution, all shift information must be written in a .txt file named "employees_log.txt",
    on the same directory as the solution "pyment_manager.py".

Employee's shif hours must be written in the following format:

NAME=DWHH:MM-HH:MM,DWHH:MM-HH:MM,...

DW = Day of week (MO, TU, WE, TH, FR, SA, SU)
HH = Hour, with two digits
MM = Minutes, with two digits
Starting and ending working hours are separated by the hyphen "-"
Example log:

ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00 RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00


Output:

The salary of ALFRED for this month is: 340.0 USD
The salary of JUNIOR for this month is: 720.0 USD
The salary of NINA for this month is: 343.75 USD
The salary of LUCASBAYOUT for this month is: 795.0 USD
The salary of ASTRID for this month is: 85.0 USD