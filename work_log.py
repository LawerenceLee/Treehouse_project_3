# work_log.py
import datetime as dt
import pytz
import csv
import os
import re
import collections

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


def __search_csv(search_param, date_choice=None, minutes=None, keywords=None, regex=None):
    with open('work_log.csv',newline='') as csvfile:
        logreader = csv.DictReader(csvfile, delimiter=',')
        rows = list(logreader)
        
        if search_param == 'date':
            param_list = []
            for row in rows:
                param_list.append(row['task_date'])
            print('Task Date \n---------')
            for date in set(param_list):
                print(date)
                
        elif search_param == 'exact_date':
            __clear()
            print(' ', date_choice, 'Tasks', '\n', '-'*16)
            count = 0
            for row in rows:
                if row['task_date'] == date_choice:
                    print('Time:', row['task_time'], '\n', 
                          'Name:', row['task_name'], '\n', 
                          'Time to Complete:', row['task_minutes'], 'Minutes', '\n', 
                          'Note:', row['task_note'], '\n')
                    count += 1
            if count == 0:
                print('\nThere are no log entries for {}'.format(date_choice))
                input('Please try entering another date.')
                __date_search()
        
        elif search_param == 'time':
            param_list = []
            for row in rows:
                param_list.append(float(row['task_minutes']))
            print('Task Minutes \n---------')
            for time in sorted(set(param_list)):
                print(time, 'min')
                    
        elif search_param == 'comp_time':
            __clear()
            print(minutes, 'Minute Tasks', '\n', '-'*14)
            count = 0
            for row in rows:
                if row['task_minutes'] == minutes:
                    print('Date/Time:', row['task_date'], row['task_time'], '\n',
                          'Name:', row['task_name'], '\n', 
                          'Note:', row['task_note'], '\n')
                    count += 1
            if count == 0:
                print('\nThere are no log entries with a completetion time of {} minutes'.format(minutes))
                input('Please try again.')
                __time_search()
                
        elif search_param == 'search_term':
            __clear()
            print(' Tasks with:', keywords, '\n', '-'*(11+len(keywords)))
            count = 0
            for row in rows:
                if keywords in row['task_name'] or keywords in row['task_note']:
                    print('Date/Time:', row['task_date'], row['task_time'], '\n',
                          'Name:', row['task_name'], '\n',
                          'Time to Complete:', row['task_minutes'], 'Minutes', '\n',
                          'Note:', row['task_note'], '\n')
                    count += 1
            if count == 0:
                print('\nThere are no log entries that contain "{}"'.format(keywords))
                input('Please try again.')
                __exact_search()
                
        elif search_param == 'pattern':
            __clear()
            print(' Tasks with: "{}" pattern\n'.format(regex), '-'*(22+len(regex)))
            count = 0
            for row in rows:
                if re.search(regex, row['task_name']) or re.search(regex, row['task_note']):
                    print('Date/Time:', row['task_date'], row['task_time'], '\n',
                          'Name:', row['task_name'], '\n',
                          'Time to Complete:', row['task_minutes'], 'Minutes', '\n',
                          'Note:', row['task_note'], '\n')
                    count += 1
            if count == 0:
                print('\nThere are no log entries that contain "{}" regex pattern'.format(regex))
                input('Please try again.')
                __pattern_search()
            

def __date_search():
    __clear()
    __search_csv('date')
    date_choice = input('\nChoose a date from above: ')
    if not re.search(r'\d\d\/\d\d/\d\d\d\d', date_choice):
        __clear()
        input('The date entered was not in the correct format, please try again.')
        __date_search()
    else:
        __search_csv('exact_date', date_choice=date_choice)
    input('\nPress "ENTER" to return to search menu.')
    __search_menu()

def __time_search():
    __clear()
    __search_csv('time')
    try:
        time_spent = input('\nPlease enter the number of minutes you would like to search by: ')
        float(time_spent)
    except ValueError:
        __clear()
        input('Please a positive numerical value.')
        __time_search()
    else:
        __search_csv('comp_time', minutes=time_spent)
    input('\nPress "ENTER" to return to search menu.')
    __search_menu()

    
def __exact_search():
    __clear()
    usr_str = input('Please enter the keyword or phrase you would to search by: ')
    __search_csv('search_term', keywords=usr_str)
    input('\nPress "ENTER" to return to search menu.')
    __search_menu()


def __pattern_search():
    __clear()
    regex = input('Please enter a valid Regex Pattern to search by: ')
    __search_csv('pattern', regex=regex)
    input('\nPress "ENTER" to return to search menu.')
    __search_menu()

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

