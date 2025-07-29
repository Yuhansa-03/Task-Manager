#Progrm Name: Task Manager - stage 3
#Author: Yuhansa Hewagamage
#UOW Number: w2153601
#Date:21 April 2025

import json

task = [] #List to store tasks in dictionary

#saving tasks to a JSON File
def save_task(file_name = "tasks.json"):
    with open("tasks.json","w") as file:
        json.dump(task,file,indent = 4) #saving the python data in the task list into a JSON file
        
#Loading tasks from the existing JSON file into the task list so it won't get overwritten
        
def load_tasks(file_name = "tasks.json"):
    try:
        with open("tasks.json","r") as file:
            loaded_task = json.load(file) #Converting JSON data to the python dictionary
            for i in loaded_task:
                task.append(i) #Adding data to the task list
    except FileNotFoundError:
        pass
#--------------------------------------------------------------------------------------------------------------------------       
#Input validation for date in dd-mm-yyyy format
def get_date(date_str):
    parts = date_str.split('-')
    
    if len(parts) != 3: #Checking if date has three parts as dd-mm-yyyy
        return False
    
    year,month,day = parts #Assigning variables to the three parts
    
    if not (day.isdigit() and month.isdigit() and year.isdigit()): #checking if day,month,year are digits
        return False
    
    year,month,day = int(year),int(month),int(day) #Converting the digits to integers and storing in list as integers
    
    #Checking correct input validation for date and months
    
    if month < 1 or month > 12 or day < 1 or day > 31:
        return False
    
    # Validating dates for months with 30 days
    if month in [4, 6, 9, 11] and day > 30:
        return False
    if month == 2 and day > 29:
        return False
    
    return True
    
   
def get_valid_date(): #Getting user input for due date and handling input validation
    while True:
        date = input("Enter due date (yyyy-mm-dd): ")
        if get_date(date):
            return date
        else:
            print("Invalid format. Please enter the date in yyyy-mm-dd format.")
            
#---------------------------------------------------------------------------------------------------------------------------
#Creating a new task

def create_task():
    
    task_name = input("Enter the task name: ")
    description = input("Enter task description: ")
    priority = input("Enter Priority Level-(High,Medium,Low): ").lower()
    due_date = get_valid_date()
    
    #Storing the tasks in a dictionary caled n_task 
    n_task = {"name":task_name,"description":description,"priority":priority,"due_date":due_date} 
    
    task.append(n_task) #Adding the task in the dictionary to a list
    
    #Saving the new tasks in the dictionary to the JSON file
    save_task()
    
    print(f"\nTask '{task_name}' added successfully!\n") #Informing user
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Viewing the existing tasks
def display_task():
    if not task: #Used to check if a list is empty, if it is empty it returns True
        print("No Tasks Available")
        return #Prevents the code from running further if there is no tasks and exits the function
    
    # If tasks are found, print the task list
    print("\nTask List:")
    for index, n_task in enumerate(task, start=1):
        print(f"{index}. Task Name: {n_task['name']}, Description: {n_task['description']}, Priority: {n_task['priority']}, Due Date: {n_task['due_date']}")
    print() #Used for the cleanliness of the code to leave a space after the tasks are viewed
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------    
#Function to update a task
    
def update_task():
    while True:
        display_task()
        if not task:
            return
        
        try:
            index = int(input("Enter a task number to update: ")) - 1 
            if index < 0 or index >= len(task): #Checking if the index is in correct range
                print("Invalid Input. Please enter a valid task number.")
                
                choice = input("Would you like to try again? (Y/N): ")
                if choice.lower() != 'y':
                    print("Exiting without updating.")
                    break  
                continue  
            
            print("\nUpdating Task.....") 
            
            #Updating tasks
            task[index]["name"] = input("Enter new task name: ")
            task[index]["description"] = input("Enter new description: ")
            task[index]["priority"] = input("Enter new priority - (High/Medium/Low): ")
            task[index]["due_date"] = get_valid_date()  
            
            # Saving updated tasks to file
            save_task()
            
            print("\nTask updated successfully!")
            break  
        
        except ValueError:
            print("Please enter a valid number. Try again!")
            choice = input("Would you like to try again? (Y/N): ")
            if choice.lower() != 'y':
                print("Exiting without updating.")
                break  
#-------------------------------------------------------------------------------------------------------------------------------------------
# Function to delete a task
def delete_task():
    while True:
        display_task()
        if not task:
            return
        
        try:
            index = int(input("Enter task number to delete: ")) - 1
            if index < 0 or index >= len(task): #Checking if the index is in correct range
                print("Invalid Task Number!")
                
                choice = input("Would you like to try again? (Y/N): ") #Asking user if they want to delete the task or change the choice
                if choice.lower() != 'y':
                    print("Exiting without deleting.")
                    break  
                continue  
            
            del task[index]  # Deleting the task
            
            save_task()  # Saving remaining tasks after deleting
            
            print("Task Deleted Successfully!")
            break  
        
        except ValueError:
            print("Please enter a valid number. Try again!")
            choice = input("Would you like to try again? (Y/N): ")
            if choice.lower() != 'y':
                print("Exiting without deleting.")
                break  

# Load tasks at the start of the program
load_tasks()

#----------------------------------------------------------------------------------------------------------------------------------------
# Asking user to enter a choice to select
while True:
    print("\nTask Manager :)")
    print("1. Add Task")
    print("2. View Task")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Exit")
    
    choice = input("Select a choice to proceed: ")
    
    if choice == '1':
        create_task()
    elif choice == '2':
        display_task()
    elif choice == '3':
        update_task()
    elif choice == '4':
        delete_task()
    elif choice == '5': #Exiting task manager if choice is 5
        print("Exiting Task Manager! Goodbye!")
        break
    else:
        print("Invalid choice. Try Again!")   
   
    
    
