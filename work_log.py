# work_log.py
import datetime as dt
import csv
import os
import re
import sys


def __check_for_log():
    """
    Checks for work_log.csv in the current directory, and creates
    the csv file with defined fieldnames if it is not found.
    """
    if 'work_log.csv' not in os.listdir(os.getcwd()):
        with open('work_log.csv', 'a') as csvfile:
            fieldnames = ['task_date', 'task_time', 'task_name', 'task_minutes', 'task_note']
            itemwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            itemwriter.writeheader()


def __clear():
    """
    Clears the terminal screen.
    """
    os.system("cls" if os.name == "nt" else "clear")

# Editing Records
###############################################################################


def __editing_csv(var_dict, index):
    """
    The function copies all records other than the one passed as an argument to a
    new csv file. The function will add the edited record if that option is
    selected to the new csv file. Upon completion of the aformentioned, the
    function deletes the original csv, and renames the new csv to match
    the original filename.
    """
    with open('work_log.csv', mode='r') as input_file, open('edited_work_log.csv', mode='w') as output_file:
        fieldnames = ['task_date', 'task_time', 'task_name', 'task_minutes', 'task_note']
        log_writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        log_writer.writeheader()

        for row in list(csv.DictReader(input_file, delimiter=',')):
            if var_dict[index]['task_note'] == row['task_note'] and var_dict[index]['task_name'] == row['task_name']:
                edit_quest = input('\nWould you simply like to simply [D]elete the record, or [E]dit it? ').upper()
                if edit_quest == 'D':
                    input('Entry will be deleted. \n\nPress ENTER to Continue. ')
                    pass
                else:
                    name_quest = input('Do you wish to change the name of the task? [y/N] ').upper()
                    if name_quest == 'Y':
                        edited_name = input('Enter your new task name: ')
                    else:
                        edited_name = var_dict[index]['task_name']

                    minutes_quest = input('Do you wish to change the number of minutes to complete the task? [y/N] ').upper()
                    if minutes_quest == 'Y':
                        edited_minutes = input('Enter the new number of minutes for your task (integers only): ')
                        edited_minutes = int(edited_minutes)
                    else:
                        edited_minutes = var_dict[index]['task_minutes']

                    note_quest = input('Would you like to edit your note from this task? [y/N] ').upper()
                    if note_quest == 'Y':
                        edited_note = input('Enter your new note: ')
                    else:
                        edited_note = var_dict[index]['task_note']

                    log_writer.writerow({
                                    'task_date': var_dict[index]['task_date'],
                                    'task_time': var_dict[index]['task_time'],
                                    'task_name': edited_name,
                                    'task_minutes': edited_minutes,
                                    'task_note': edited_note
                                    })
            else:
                log_writer.writerow({
                                    'task_date': row['task_date'],
                                    'task_time': row['task_time'],
                                    'task_name': row['task_name'],
                                    'task_minutes': row['task_minutes'],
                                    'task_note': row['task_note']
                                    })

        for filename in os.listdir(os.getcwd()):
            if filename == 'work_log.csv':
                os.remove('work_log.csv')
        for filename in os.listdir(os.getcwd()):
            if filename == 'edited_work_log.csv':
                os.renames('edited_work_log.csv', 'work_log.csv')


# Record Input Function
###############################################################################

def __input_menu():
    """
    This function prompts user for the various details to create a record of a
    task, and then saves them to the csv file associated with the program.
    """
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
###############################################################################

def record_print(catagory_list, index):
    """
    This function prints out the details of the task record passed as an
    argument, as well as the number of records in the ordered dictionary passed
    to the function.
    """
    __clear()
    print('Date/Time:', catagory_list[index]['task_date'], catagory_list[index]['task_time'], '\n',
          'Name:', catagory_list[index]['task_name'], '\n',
          'Time to Complete:', catagory_list[index]['task_minutes'], 'Minutes', '\n',
          'Note:', catagory_list[index]['task_note'], '\n')
    print('{}/{} Records\n'.format(index+1, len(catagory_list)))


def page_thru(var_dict):
    """
    This function facilitates the paging through the various records matching
    the search query performed earlier while using the program. It also allows
    user to enter an editing interface for the current record being displayed.
    """
    index = 0
    while True:
        page_option = input('[F]orward, [B]ack, [E]dit/Delete, [S]earch Menu: ').upper()
        if page_option == 'F':
            try:
                index += 1
                record_print(var_dict, index)
            except KeyError:
                input("You've reached the Last Record \n\nPress ENTER to return to it.")
                index -= 1
                record_print(var_dict, index)
        elif page_option == 'B':
            try:
                index -= 1
                record_print(var_dict, index)
            except KeyError:
                input("You've reached the Beginning of the Records \n\nPress ENTER to return to the First Record.")
                index += 1
                record_print(var_dict, index)
        elif page_option == 'E':
            __editing_csv(var_dict, index)
            break
        elif page_option == 'S':
            break
    __search_menu()


# Finding Records in CSV
###############################################################################

def __search_csv(search_param, date_choice=None, minutes=None, keywords=None, regex=None, start_date=None, end_date=None):
    """
    This function facilitates the various ways to perform queries of the csv file
    that contains the records of work tasks.
    """
    with open('work_log.csv', newline='') as csvfile:
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
###############################################################################


def __date_search():
    """
    This function presents users a list of available dates in the csv file,
    and allows them to choose one.
    """
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
    """
    This function allows users to specify a date range to query the csv file
    with.
    """
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
    """
    This function allows users to query the csv file by choosing from a list of
    times (in minutes) of various task completion times that exist in the csv
    file.
    """
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
    """
    Function lets users query csv file with a specific phrase or keyword.
    """
    __clear()
    usr_str = input('Please enter the keyword or phrase you would to search by: ')
    __search_csv('search_term', keywords=usr_str)


def __pattern_search():
    """
    Function lets users query csv file with a specific regex.
    """
    __clear()
    regex = input('Please enter a valid Regex Pattern to search by: ')
    __search_csv('pattern', regex=regex)

# Menus
###############################################################################


def __search_menu():
    """
    Function presents users with the various methods they can use to query
    the csv file, and allows them to choose one.
    """
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
    else:
        input('The input provided does not match a menu option, please try again. ')
        __search_menu()


def __main_menu():
    """
    Function allows users to choose between adding new records or
    perusing/editing old ones.
    """
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

###############################################################################

if __name__ == '__main__':
    __check_for_log()
    __main_menu()
