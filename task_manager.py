# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.


#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass


# Parses through tasks.txt and creates a list of dictionaries with descriptive keys for parts of each line
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

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
        new_username = input("New Username: ")

        # Check to prevent duplicate usernames
        if new_username in username_password.keys():
            print("Username already exists please try again")
            continue

        # - Request input of a new password and confirmation password
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")

        # Adds user if password successfully confirmed
        if new_password == confirm_password:
            print("New user added")
            username_password[new_username] = new_password
            
            # Writes changes to user.txt file
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
            break

        # Error message if passwords don't match
        else:
            print("Passwords do not match")
            continue


def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
            - User assigned to task
            - Title of a task
            - Description of the task
            - Due date of the task.'''
    while True:
        # Asks user for user assigned to task and checks user is registered
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist please enter a valid username")
            continue
        else:
            break
    
    # Asks user for task title and description
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    #Asks user for task due date and checks format is correct
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format please use the format specified")

    # Get current date to add to task details
    curr_date = date.today()

    # Creates dictionary to be appended to task_list
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    
    # Writes changes to task_list to tasks.txt file
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
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) '''

    for t in task_list:
        disp_str = "-" * 75 + "\n"
        disp_str += f"Task: \t {t['title']}\n"
        disp_str += f"\nAssigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Completed: \t {t['completed']}\n"
        disp_str += f"\nTask Description: \n{t['description']}"
        disp_str += f""
        print(disp_str)
    print("-" * 75)


"""
Presents users currently assigned tasks allowing them to:
- mark as complete / incomplete
- reassign it to another user
- change its due date
"""
def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)'''

    # Variables to track task lines and display to user
    i = 0
    display_count = 1
    indices = []

    # Displays task details to user and appends indices of tasks into list
    for t in task_list:
        if t['username'] == curr_user:
            disp_str = "-" * 75 + "\n"
            disp_str += f"Task {display_count}: \t {t['title']}\n"
            disp_str += f"\nAssigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Completed: \t {t['completed']}\n"
            disp_str += f"\nTask Description: \n{t['description']}"
            disp_str += f""
            print(disp_str)
            indices.append(i)
            display_count += 1
        i += 1
    print("-" * 75)

    # Prompts user for task selection based on output
    while True:
        try:
            # Minuses by one to match selection to list indices
            selection = int(input("Please select a task: ")) - 1
            if selection not in range(len(indices)):
                print("Task out of range\n")
                continue
            else:
                break
        except ValueError:
            print("Please enter a whole number\n")

    # Prompts user to select action for selected task
    while True:
        task_menu = input(f"""\nSelect one of the following options below for task {selection + 1}:
c - Mark task as complete / incomplete
ed - Edit task due date
ea - Edit task assignee
e - exit
:""").lower()
        
        # Changes task completion status to opposite in task_list
        if task_menu == "c":
            if task_list[indices[selection]]['completed'] == False:
                task_list[indices[selection]]['completed'] = True
                print(f"Task {selection + 1} marked as complete")
            else:
                task_list[indices[selection]]['completed'] = False
                print(f"Task {selection + 1} marked as incomplete")


        # Changes task due date in task_list
        elif task_menu == "ed":

            # Prevents editing if task already complete
            if task_list[indices[selection]]['completed'] == True:
                print("Completed tasks cannot be edited")
                continue

            due_date = input(f"\nDue date of task {selection + 1} (YYYY-MM-DD): ")

            # Defensive programming to ensure input in proper date format
            try:
                task_list[indices[selection]]['due_date'] = datetime.strptime(due_date, DATETIME_STRING_FORMAT)
                print(f"Task {selection + 1} due date changed")
            except ValueError:
                print("Invalid datetime format. Please use the format specified")


        # Changes user assigned to task
        elif task_menu == "ea":

            # Prevents editing if task already complete
            if task_list[indices[selection]]['completed'] == True:
                print("Completed tasks cannot be edited")

            task_username = input(f"\nPlease enter the username of the person you would like to assign task {selection + 1} to: ")

            # Checks if input matches registered users and reassigns user if it is
            if task_username not in username_password.keys():
                print("User does not exist")
                continue
            else:
                task_list[indices[selection]]['username'] = task_username
                print(f"Task {selection + 1} assigned to {task_username}")
        
        # Exits task editor
        elif task_menu == "e":
            print("Exiting task editor")
            break

        else:
            print("Please select a listed option")
        

        # Writes all modifications to tasks_lists to text file
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


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.'''

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()        

    elif menu == 'vm':
        view_mine()
    
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")