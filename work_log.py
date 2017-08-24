# work_log.py
import datetime as dt
import pytz
import csv
import os

def __check_for_log():
    if 'work_log.csv' not in os.listdir(str(os.getcwd())):
        with open('work_log.csv', 'a') as csvfile:
            fieldnames = ['task_date', 'task_time', 'task_name', 'task_minutes', 'task_note']
            itemwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            itemwriter.writeheader()

def __clear():
    os.system("cls" if os.name == "nt" else "clear")

def input_menu():
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
    main_menu()

def date_search():
    # provide a list of dates with entries
    # user chooses a date to view 
    pass
        
def time_search():
    # user enters a number for min spent on task
    # return a list of entries
    # user picks from list
    pass
    
def exact_search():
    # user enters a str 
    # return a list of entries containing all of such string
    # user picks from list
    pass

def pattern_search():
    # user enters a regex pattern
    # return a list of entries contain such pattern
    # user picks from list
    pass

def search_menu():
    # find by date
        # date_search()
    # find by time spent
        # time_search()
    # find by exact search
        # exact_search()
    # find by pattern
        # pattern_search()
    pass    

def main_menu():
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
        input_menu()
    elif option_choice == 'S':
        search_menu()
    elif option_choice == 'E':
        exit
    else:
        input('The input provided does not match a menu option, please try again. ')
        main_menu()
    # menu option for adding entries
        # input menu
    # menu option for searching previous entries
        # search menu
    # exit option
    pass

if __name__ == '__main__':
    __check_for_log()
    main_menu()

