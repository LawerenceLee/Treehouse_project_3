# work_log.py
import datetime as dt
import csv
import os
import re

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

# Record Input Function
########################################################################################
    
def __input_menu():
    __clear()
    task_name = input('Enter task name: ')
    __clear()
    try:
        task_time = input('Time to complete task in minutes (integers only): ')
        int(task_time)
    except ValueError:
        __clear()
        input('Time to complete must be a whole number! ')
        __input_menu()
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

# Record Viewing Functions 
########################################################################################

def record_print(catagory_list, index):
    __clear()
    print('Date/Time:', catagory_list[index]['task_date'], catagory_list[index]['task_time'], '\n', 
          'Name:', catagory_list[index]['task_name'], '\n', 
          'Time to Complete:', catagory_list[index]['task_minutes'], 'Minutes', '\n', 
          'Note:', catagory_list[index]['task_note'], '\n')

def page_thru(var_dict):
    index = 0
    while True:
        page_option = input('[F]orward, [B]ack, [E]dit, [S]earch Menu: ').upper()
        if page_option == 'F':
            try:
                index += 1
                record_print(var_dict, index)
            except KeyError:
                input('Last Record')
                index -= 1
                record_print(var_dict, index)
        elif page_option == 'B':
            try:
                index -= 1
                record_print(var_dict, index)
            except KeyError:
                input('First Record')
                index += 1
                record_print(var_dict, index)
        elif page_option == 'E':
            pass
        elif page_option == 'S':
            break
    __search_menu()

# Finding Records in CSV
########################################################################################
    
def __search_csv(search_param, date_choice=None, minutes=None, keywords=None, regex=None, start_date=None, end_date=None):
    with open('work_log.csv', newline='', mode='a') as csvfile:
        logreader = csv.DictReader(csvfile, delimiter=',')
        rows = list(logreader)
        
        if search_param == 'date':
            param_list = []
            for row in rows:
                param_list.append(dt.datetime.strptime(row['task_date'], '%m/%d/%Y'))
            print('Task Date \n---------')
            for date in sorted(set(param_list)):
                print(date.strftime('%m/%d/%Y'))
                
        elif search_param == 'exact_date':
            date_list = []
            count = 0
            for row in rows:
                if row['task_date'] == date_choice:
                    date_list.append(row)
                    count += 1
            if count == 0:
                print('\nThere are no log entries for {}'.format(date_choice))
                input('Please try entering another date.')
                __date_search()
            date_dict = dict(enumerate(date_list))
            record_print(date_dict, 0)
            page_thru(date_dict)
            
        elif search_param == 'date_range':
            date_range_list = []
            count = 0
            for row in rows:
                if dt.datetime.strptime(row['task_date'], '%m/%d/%Y') >= start_date and dt.datetime.strptime(row['task_date'], '%m/%d/%Y') <= end_date:
                    date_range_list.append(row)
                    count += 1
            if count == 0:
                print('\nThere are no log entries between {} - {}'.format(start_date, end_date))
                input('Please try entering another set of dates.')
                __date_range_search()
            date_range_dict = dict(enumerate(date_range_list))
            record_print(date_range_dict, 0)
            page_thru(date_range_dict)
            
        elif search_param == 'time':
            param_list = []
            for row in rows:
                param_list.append(int(row['task_minutes']))
            print('Task Minutes \n---------')
            for time in sorted(set(param_list)):
                print(time, 'min')               
                    
        elif search_param == 'comp_time':
            minutes_list = []
            count = 0
            for row in rows:
                if row['task_minutes'] == minutes:
                    minutes_list.append(row)
                    count += 1
            if count == 0:
                print('\nThere are no log entries with a completetion time of {} minutes'.format(minutes))
                input('Please try again.')
                __time_search()
            minute_dict = dict(enumerate(minutes_list))
            record_print(minute_dict, 0)
            page_thru(minute_dict)

        elif search_param == 'search_term':
            keyword_list = []
            count = 0
            for row in rows:
                if keywords in row['task_name'] or keywords in row['task_note']:
                    keyword_list.append(row)
                    count += 1
            if count == 0:
                print('\nThere are no log entries that contain "{}"'.format(keywords))
                quest_to_menu = input('\n[S]earch Menu, "Enter" for try again: ').upper()
                if quest_to_menu == 'S':
                    __search_menu()
                __exact_search()
            keyword_dict = dict(enumerate(keyword_list))
            record_print(keyword_dict, 0)
            page_thru(keyword_dict)


        elif search_param == 'pattern':
            pattern_list = []
            count = 0
            for row in rows:
                if re.search(regex, row['task_name']) or re.search(regex, row['task_note']):
                    pattern_list.append(row)
                    count += 1
            if count == 0:
                print('\nThere are no log entries that contain "{}" regex pattern'.format(regex))
                input('Please try again.')
                __pattern_search()
            pattern_dict = dict(enumerate(pattern_list))
            record_print(pattern_dict, 0)
            page_thru(pattern_dict)

# Search Functions
########################################################################################

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

def __date_range_search():
    __clear()
    start_date = input('Enter a starting date for search (using MM/DD/YYYY): ')
    end_date = input('Enter a ending date for search (using MM/DD/YYYY): ')
    if not re.search(r'\d\d\/\d\d/\d\d\d\d', start_date) or not re.search(r'\d\d\/\d\d/\d\d\d\d', end_date):
        __clear()
        input('Either the start or end date was not entered in the correct format, please try again.')
        __date_range_search()
    else:
        start_date = dt.datetime.strptime(start_date, '%m/%d/%Y')
        end_date = dt.datetime.strptime(end_date, '%m/%d/%Y')
        __search_csv('date_range', start_date=start_date, end_date=end_date)

def __time_search():
    __clear()
    __search_csv('time')
    try:
        time_spent = input('\nPlease enter the number of minutes you would like to search by (integers only): ')
        int(time_spent)
    except ValueError:
        __clear()
        input('Please a positive numerical value.')
        __time_search()
    else:
        __search_csv('comp_time', minutes=time_spent)
    
    
def __exact_search():
    __clear()
    usr_str = input('Please enter the keyword or phrase you would to search by: ')
    __search_csv('search_term', keywords=usr_str)
    

def __pattern_search():
    __clear()
    regex = input('Please enter a valid Regex Pattern to search by: ')
    __search_csv('pattern', regex=regex)

# Menus
########################################################################################
    
def __search_menu():
    __clear()
    print('SEARCH MENU')
    print("""
    -- Options --
    [D] : Search by Date
    [G] : Search by Date Range
    [T] : Search by Time Spent
    [K] : Search with specific Keyword or phrase
    [R] : Search with a Regular Expression
    [M] : MAIN MENU
    [E] : EXIT
    """)
    search_choice = input("Please select an option from above: ").upper()
    if search_choice == 'D':
        __date_search()
    elif search_choice == 'G':
        __date_range_search()
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

########################################################################################

if __name__ == '__main__':
    __check_for_log()
    __main_menu()

