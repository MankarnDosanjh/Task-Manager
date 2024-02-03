# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.


#=====importing libraries===========
import os
from datetime import datetime, date
import random
import time

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

# Creates list including all tasks from tasks.txt
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# Iterates through tasks and creates dictionaries for each and appends to a list
task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Functions====
def reg_user():
    '''Add a new user to the user.txt file'''
    
    while True:
        new_username = input("\nNew Username: ")

        # Check to prevent duplicate usernames
        if new_username in username_password.keys():
            print("ERROR - Username already exists")
            continue

        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

        # Registers changes if password confirmed
        if new_password == confirm_password:
            username_password[new_username] = new_password
            
            # Writes changes to user.txt file
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
            print("New user added")
            break

        else:
            print("ERROR - Passwords do not match")


def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
            - User assigned to task
            - Title of a task
            - Description of the task
            - Due date of the task'''
    
    # Prompts for user assigned to task and checks user exists
    while True:
        task_username = input("\nName of person assigned to task: ")
        if task_username not in username_password.keys():
            print("ERROR - User does not exist")
        else:
            break
    
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    # Prompts for task due date and checks format is appropriate
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("ERROR - Invalid datetime format")

    curr_date = date.today()

    # Dictionary to be appended to task list
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    
    # Writes changes to tasks.txt file
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added")


def view_all():
    '''Reads tasks from tasks.txt file and presents them to user'''

    # Fake loading bar helps user distinguish old from new output
    for s in range(50):
        print(".", end = "")
        time.sleep(random.random() / 10)
    print("")

    # Iterates through task list and prints out task details
    for t in task_list:
        disp_str = "-" * 75 + "\n"
        disp_str += f"Task: \t\t {t['title']}\n"
        disp_str += f"\nAssigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Completed: \t {"Yes" if t['completed'] == True else "No"}\n"
        disp_str += f"\nTask Description: \n{t['description']}"
        disp_str += f""
        print(disp_str)
    print("-" * 75)


def view_mine():
    '''Reads tasks of current user and allows user to:
        - Mark tasks as complete
        - Change task due dates
        - Reassign their tasks to other users'''

    while True:
        # Used to store index of task in task_list
        i = 0

        # Used to store relevant indices
        indices = []

        # Tracks user task count in numerical order
        display_count = 1

        # Fake loading bar helps user distinguish old from new output
        print("\nLOADING")
        for s in range(50):
            print(".", end = "")
            time.sleep(random.random() / 10)
        print("")

        # Displays task details to user and stores indices of tasks
        for t in task_list:
            if t['username'] == curr_user:
                disp_str = "-" * 75 + "\n"
                disp_str += f"Task {display_count}: \t {t['title']}\n"
                disp_str += f"\nAssigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Completed: \t {"Yes" if t['completed'] == True else "No"}\n"
                disp_str += f"\nTask Description: \n{t['description']}"
                disp_str += f""
                print(disp_str)

                # Stores task index and increments count for tasks displayed to user
                indices.append(i)
                display_count += 1

            i += 1
        print("-" * 75)

        # Prompts user for task selection
        try:
            selection = int(input("Please select a task (type -1 to exit task viewer): "))
            if selection == -1:
                break
            
            # Minus by one to match selection with index
            selection -= 1

            # Checks if selection is within number of tasks
            if selection not in range(len(indices)):
                print("ERROR - Task out of range")
                continue

        # Error message when non-int entered
        except ValueError:
            print("ERROR - Enter a whole number")
            continue

        # Prompts user for action to be performed on task
        task_menu = input(f"""\nSelect one of the following options below for task {selection + 1} (to deselect type anything else):
c - Mark task as complete / incomplete
a - Edit task assignee
d - Edit task due date
:""").lower()
            
        # Changes task completion status to opposite in task_list
        if task_menu == "c":
            if task_list[indices[selection]]['completed'] == False:
                task_list[indices[selection]]['completed'] = True
                print(f"Task {selection + 1} marked as complete")
            else:
                task_list[indices[selection]]['completed'] = False
                print(f"Task {selection + 1} marked as incomplete")

       # Changes user assigned to task
        elif task_menu == "a":

            # Prevents editing if task already complete
            if task_list[indices[selection]]['completed'] == True:
                print("Completed tasks cannot be edited")
                continue

            # Prompts for user to reassign task to, checking for non-existent usernames
            task_username = input(f"\nUser to reassign task {selection + 1} to: ")
            if task_username not in username_password.keys():
                print("User does not exist")
            else:
                task_list[indices[selection]]['username'] = task_username
                print(f"Task {selection + 1} reassigned to {task_username}")

        # Changes task due date in task_list
        elif task_menu == "d":

            # Prevents editing if task already complete
            if task_list[indices[selection]]['completed'] == True:
                print("ERROR - Completed tasks cannot be edited")
                continue

            # Prompts for new task due date and checks date format is appropriate
            due_date = input(f"\nDue date of task {selection + 1} (YYYY-MM-DD): ")
            try:
                task_list[indices[selection]]['due_date'] = datetime.strptime(due_date, DATETIME_STRING_FORMAT)
                print(f"Task {selection + 1} due date changed")
            except ValueError:
                print("ERROR - Invalid datetime format")
            
        else:
            print(f"Task {selection + 1} deselected")

        # Writes all modifications to tasks_lists to tasks.txt
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))


def generate_report():
    '''Generate text file reports on all tasks:
        - task_overview.txt:
            - Total number of tasks
            - Number and % of completed, incomplete and overdue tasks
            
        - user_overview.txt:
            - Total number of users
            - Total number of tasks
            - Number and % of completed, incomplete and overdue tasks for each individual user
            
    # PROLIFIC USE OF GET PREVENTS ERRORS WHEN TASKS OF A CERTAIN TYPE DO NOT EXIST'''
    
    # Stores number of complete, incomplete and overdue tasks
    total_complete = 0
    total_incomplete = 0
    total_overdue = 0
    
    # Stores number of complete, incomplete and overdue tasks with user as key and number of specific tasks as value
    user_complete = {}
    user_incomplete = {}
    user_overdue = {}
    user_total = {}

    for task in task_list:

        # Tracks overdue tasks
        if task['completed'] == False and task['due_date'] < datetime.today():
            user_overdue[task['username']] = user_overdue.get(task['username'], 0) + 1
            user_incomplete[task['username']] = user_incomplete.get(task['username'], 0) + 1
            total_overdue += 1
            total_incomplete += 1
        
        # Tracks completed tasks
        elif task['completed'] == True:
            user_complete[task['username']] = user_complete.get(task['username'], 0) + 1
            total_complete += 1

        # Tracks incomplete tasks
        else:
            user_incomplete[task['username']] = user_incomplete.get(task['username'], 0) + 1
            total_incomplete += 1
        
        # Updates users task total count
        user_total[task['username']] = user_complete.get(task['username'], 0) + user_incomplete.get(task['username'], 0)
    
    # Calculates total number of tasks
    task_total = total_complete + total_incomplete
    
    # Creates task report in task_overview.txt
    with open("task_overview.txt", "w") as fhandle:
        fhandle.write(f"Total task count: \t{task_total}")
        fhandle.write(f"\nCompleted tasks: \t{total_complete} ({int((total_complete / task_total) * 100) if task_total != 0 else 0}%)")
        fhandle.write(f"\nIncomplete tasks: \t{total_incomplete} ({int((total_incomplete / task_total) * 100) if task_total != 0 else 0}%)")
        fhandle.write(f"\nOverdue tasks: \t\t{total_overdue} ({int((total_overdue / task_total) * 100) if task_total != 0 else 0}%)")
    
    # Creates user report in user_overview.txt
    with open("user_overview.txt", "w") as fhandle:

        fhandle.write(f"Total number of registered users: {len(username_password)}")
        fhandle.write(f"\nTotal number of tasks: {task_total}\n")
        
        # Iterates through usernames and writes user reports to user_overview.txt
        for user in username_password.keys():
            disp_str = "\n"
            disp_str += f"{user}'s Task Overview:"
            disp_str += "\n" + "-" * 50
            disp_str += f"\nTotal task count: \t{user_total.get(user, 0)} ({int((user_total.get(user, 0) / task_total) * 100) if task_total != 0 else 0}%)"
            disp_str += f"\nCompleted tasks: \t{user_complete.get(user, 0)} ({int((user_complete.get(user, 0) / user_total.get(user, 1)) * 100)}%)"
            disp_str += f"\nIncomplete tasks: \t{user_incomplete.get(user, 0)} ({int((user_incomplete.get(user, 0) / user_total.get(user, 1)) * 100)}%)"
            disp_str += f"\nOverdue tasks: \t\t{user_overdue.get(user, 0)} ({int((user_overdue.get(user, 0) / user_total.get(user, 1)) * 100)}%)"
            disp_str += "\n"

            fhandle.write(disp_str)

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.'''

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Creates dictionary pair of username / password from user.txt
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

# Prompts user to login, checking username and password match
logged_in = False
while not logged_in:

    print("\nLOGIN")
    curr_user = input("Username: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    curr_pass = input("Password: ")
    
    if username_password[curr_user] != curr_pass:
        print("Wrong password")
    else:
        print("Login successful")
        logged_in = True

# Displays options to user and executes selected option
while True:
    print()
    menu = input('''Select one of the following options below:
r  - register user
a  - add task
va - view all tasks
vm - view my tasks
gr - generate reports
e  - exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()        

    elif menu == 'vm':
        view_mine()

    elif menu == "gr":
        generate_report()

    elif menu == 'e':
        print('Goodbye')
        exit()

    else:
        print("ERROR - Please select a displayed option")