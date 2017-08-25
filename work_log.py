# work_log.py
import datetime as dt
import pytz
import csv
import os

def __check_for_log():
    """
    Checks for work_log.csv in the current directory, and creates
    the csv file with defined fieldnames if it is not found.
    """
    if 'work_log.csv' not in os.listdir(str(os.getcwd())):
        with open('work_log.csv', 'a') as csvfile:
            fieldnames = ['task_date', 'task_time', 'task_name', 'task_minutes', 'task_note']
            itemwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            itemwriter.writeheader()

def __clear():
    """
    Clears the terminal screen.
    """
    os.system("cls" if os.name == "nt" else "clear")

def __input_menu():
    __clear()
    task_name = input('Enter task name: ')
    __clear()
    task_time = input('Time to complete task in minutes: ')
    task_note = ''
    __clear()
    add_note_quest = input('Would you like to add any additional notes [y/N]: ').upper()
    if add_note_quest == 'Y':
        __clear()
        task_note = input('Enter additional notes: ') 
    
    with open('work_log.csv', 'a') as csvfile:
        fieldnames = ['task_date', 'task_time', 'task_name', 'task_minutes', 'task_note']
        itemwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        itemwriter.writerow({
            'task_date': dt.datetime.now().strftime('%m/%d/%Y'),
            'task_time': dt.datetime.now().strftime('%H:%M'),
            'task_name': task_name,
            'task_minutes': task_time,
            'task_note': task_note
        })
    __main_menu()

def __list_printout(search_param):
    __clear()
    # takes in a search type perameter (by date, time spent, pattern)
    # prints out a list of dates with unique number identifiers
    pass

def __entry_printout():
    __clear()
    pass

def __date_search():
    __clear()
    # provide a list of dates
    date_choice = input('Choose a date from above: ')
    # returns all entries with date_choice

def __time_search():
    __clear()
    time_spent = input('Please enter the number of minutes you would like to search by: ')
    # user enters a number for min spent on task
    # return a list of entries
    # user picks from list
    
def __exact_search():
    __clear()
    usr_str = input('Please enter the keyword or phrase you would to search by: ')
    # user enters a str 
    # return a list of entries containing all of such string
    # user picks from list

def __pattern_search():
    __clear()
    pattern = input('Please enter a valid Regex Pattern to search by: ')
    # searches csv with regex, and returns a list of entries
    # if list is empty the user is alerted and presented with an option to return to 
    # try another regex search, return to search menu, or exit.
    # user picks from list

def __search_menu():
    __clear()
    print('SEARCH MENU')
    print("""
    -- Options --
    [D] : Search by Date
    [T] : Search by Time Spent
    [K] : Search with specific Keyword or phrase
    [R] : Search with a Regular Expression
    [M] : MAIN MENU
    [E] : EXIT
    """)
    search_choice = input("Please select an option from above: ").upper()
    if search_choice == 'D':
        __date_search()
    elif search_choice == 'T':
        __time_search()
    elif search_choice == 'K':
        __exact_search()
    elif search_choice == 'R':
        __pattern_search()
    elif search_choice == 'M':
        __main_menu()
    elif search_choice == 'E':
        exit
    else:
        input('The input provided does not match a menu option, please try again. ')
        __search_menu()
    

def __main_menu():
    __clear()
    print('WORK LOGGER')
    print("""
    -- Options --
    [N] : New Entry
    [S] : Search Entries
    [E] : EXIT
    """)
    option_choice = input("Please select an option from above: ").upper()
    if option_choice == 'N':
        __input_menu()
    elif option_choice == 'S':
        __search_menu()
    elif option_choice == 'E':
        exit
    else:
        input('The input provided does not match a menu option, please try again. ')
        __main_menu()

if __name__ == '__main__':
    __check_for_log()
    __main_menu()
