from datetime import time, datetime, date, timedelta
from collections import defaultdict

class Salary:
    RATES = {"weekday": {"shift_1": 25,         # A dictionary of dictionaries, with rates for each shift for weekdays and weekends
                         "shift_2": 15,
                         "shift_3": 20},
             "weekend": {"shift_1": 30,
                         "shift_2": 20,
                         "shift_3": 25}
    }

    WEEKDAYS = ("MO", "TU", "WE", "TH", "FR")

    SHIFT_RANGE = {"shift_1": (time(hour=0, minute=0, second=1),
                               time(hour=9, minute=0)),
                   "shift_2": (time(hour=9, minute=0, second=1),
                               time(hour=18, minute=0)),
                   "shift_3": (time(hour=18, minute=0, second=1),
                               time(hour=23, minute=59, second=59))}

    @staticmethod
    def load_shifts(path: str) -> set: #reads from the log file,  creating a new employee instance for each line.
        employee_set = set()
        with open(path) as file:
            for line in file.read().splitlines():
                name, data = line.split("=") #It just splits by the "=" and uses the left element as the name input, and right element as the shift input of the employee class.
                employee_set.add(Employee(name,data)) #add instead of apendd because we are dealing with a set
        return employee_set #retorna uma tupla

    @classmethod
    def calculation(cls, day: str, shift: tuple) -> float: #checks if the inputted day is a weekday or weekend and then,
        compensation = 0                                                #at this point
        if day in cls.WEEKDAYS:
            week_flag = "weekday"
        else:
            week_flag = "weekend"   #by calling the slice_shift method,
        for shift_name, hours in cls.slice(shift).items():# it can iterate through all shifts worked on that day and calculate the correct compensation
            compensation += hours * cls.RATES[week_flag][shift_name] # If recruiter has doubt, remember him that it just mean a self for a class method.
        return compensation

    @classmethod
    def update(cls, employees: set) -> set: #calls the calculate_compensation method for each shift in each day for each employee on the inputted set,

        for employee in employees:
            credit = 0
            for day, shifts in employee.shift_data.items():
                for shift in shifts:
                    credit += cls.calculation(day, shift) # and updates their credit attribute.
            employee.credit += credit

    @classmethod
    def slice(cls, shift: tuple) -> dict: #Takes starting and ending hours in a day, and then
        hours_per_shift = dict()
        for shift_number, shift_range in cls.SHIFT_RANGE.items():
            lower = datetime.combine(date.min,max(shift[0], shift_range[0]))
            upper = datetime.combine(date.min,min(shift[1], shift_range[1]))
            hours = max(upper - lower, timedelta(0))
            hours_per_shift[shift_number] = round(hours.total_seconds()/3600,2)    #returns how much hours have been worked in each separated shift.
        return hours_per_shift


class Employee:
    def __init__(self, name:str, shift_data:str): #constructor class for employee
        self.name = name
        self.shift_data = self.parse_shift(shift_data)
        self.credit = 0

    def __str__(self) -> str:
        return f"Employee: {self.name} Credit: {self.credit}"

    @staticmethod
    def parse_shift(shift_data:str) -> defaultdict: #initialization of an employee instance and it splits the shift string by the "," and then,
        parsed_shifts = defaultdict(list)
        for record in shift_data.split(","): #for each element, it takes the first two characters to identify the day and the remaining is splitted by the "-" to get starting and ending working hours.
            day, shift = record[:2], record[2:]
            start, end = shift.split("-")
            start = datetime.strptime(start, "%H:%M").time()
            end = datetime.strptime(end, "%H:%M").time()#Working hours are then converted to datetime objects.
            parsed_shifts[day].append((start, end))# parse_shift returns a defaultidict with days as keys and a tuple (start, end) hours as values.
        return parsed_shifts


if __name__ == "__main__":
    pm = Salary() #inititialization
    employees = pm.load_shifts("employees_log.txt") #reading/loading log values
    pm.update(employees)#calculating compensation


    for employee in employees:
        print(f"The salary of {employee.name} for this month is: {employee.credit} USD") #message