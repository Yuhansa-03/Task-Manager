import json
import tkinter as tk #To create windows,buttons etc
from tkinter import ttk #To create modified designs like trr view
from datetime import datetime #used to store task by due date

#definig the task class - define what a task is 
class Task: #object
    def __init__(self,name,description,priority,due_date): #we use self to store and acess the tasks inside the object
        self.name = name #storing the name in the object
        self.description = description
        self.priority = priority
        self.due_date = due_date
        
    def to_dict(self): #converting tasks to a dictionary and saving files
        return {
            'name':self.name,
            'description':self.description,
            'priority':self.priority,
            'due_date':self.due_date
            }
        
       
#defining the task manager class - to manage tasks like loading,filtering,sorting tasks
class TaskManager:
    def __init__(self,json_file='tasks.json'): #If no file is given it will use "tasks.json" by default,This file will store our task data.

        self.json_file = json_file #saves file name inside the object TaskManager
        self.tasks = [] #creates an empty list where tasks are stored
        self.load_tasks_from_json() #Loads tasks from json file to the list
        
    def load_tasks_from_json(self):

        try:
            with open(self.json_file, 'r') as file: #opens the json file in read mode
                data_task = json.load(file) #reads the task and turn it into a python dictioanry
                for task_dict in data_task: #reads each task in the dictioanry
                    task = Task(**task_dict) #Creates a new Task object from the dictionary. 
                    self.tasks.append(task) #add task object to the list
        except FileNotFoundError:
            self.tasks = [] #if file doesnt exist creates an empty task
         
         
    def get_filtered_tasks(self, name_filter=None, priority_filter=None, due_date_filter=None): #Used to search or filter tasks
        filtered = self.tasks #starts with all tasks
        
        if name_filter: #if a name is given make it lowercase and check if its inside the task name
            filtered = [item for item in filtered if name_filter.lower() in item.name.lower()]
        
        if priority_filter and priority_filter != "All": #If a priority is selected (and it’s not “All”), return only tasks that match that priority.
            filtered = [item for item in filtered if item.priority.lower() == priority_filter.lower()]
            
        if due_date_filter:#Checks if the task has the same due date.
            filtered = [item for item in filtered if item.due_date == due_date_filter]
        return filtered
            

    def sort_tasks(self, sort_key='name'): #If no value is passed it will default to sorting by name
        if sort_key == 'due_date':
            self.tasks.sort(key=self.get_due_date)
        else:
            self.tasks.sort(key=self.get_attribute_key(sort_key))

    def get_due_date(self, task): 
        return datetime.strptime(task.due_date, '%Y-%m-%d')

    def get_attribute_key(self, attr):
        def key_function(task):
            return getattr(task, attr).lower()
        return key_function
    
    
# Define the GUI class
class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager - Yuhansa Hewagamage")
        self.task_manager = TaskManager()
        self.setup_gui()
        self.populate_tree()

    def setup_gui(self): # Label and Entry for filtering by name

        tk.Label(self.root, text="task manager gui", font=("Copperplate Gothic Bold", 16, "bold")).grid(row=0, column=0, columnspan=7, pady=10)
        tk.Label(self.root, text="Filter from name:").grid(row=1, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=1, column=1, padx=5)

        # Label and dropdown (combobox) for filtering by priority
        tk.Label(self.root, text="Priority:").grid(row=1, column=2)
        self.priority_var = tk.StringVar() # Holds selected priority
        self.priority_combobox = ttk.Combobox(self.root, textvariable=self.priority_var, values=["All", "High", "Medium", "Low"])  # Options for priority to get filtered
        self.priority_combobox.current(0) # Setting default to "All"
        self.priority_combobox.grid(row=1, column=3, padx=10)

        # Label and Entry for filtering by due date
        tk.Label(self.root, text="Deadline (YYYY-MM-DD):").grid(row=1, column=4) 
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=1, column=5, padx=10)

        tk.Button(self.root, text="Filter", command=self.apply_filter).grid(row=1, column=6, padx=10)  # Filter button to apply the filters

        #Creating a Treeview  with 4 columns like a table
        self.tree = ttk.Treeview(self.root, columns=("Name", "Description", "Priority", "Due Date"), show="headings") # Only show column headings, not the default column

        #Set column headings and sorting command for each column
        for col in ["Name", "Description", "Priority", "Due Date"]:
            self.tree.heading(col, text=col, command=self.get_sort_command(col))  # Enable clicking header to sort
            self.tree.column(col, minwidth=150, width=200) #setting column size
        self.tree.grid(row=2, column=0, columnspan=7, padx=5, pady=10) # Placing the Treeview inside the window


    def get_sort_command(self, column_name): # This function returns a sorting command for a given column
        def sort_command():
            self.sort_tasks(column_name) # Call sort_tasks when column header is clicked
        return sort_command

    def populate_tree(self, tasks=None):  
        for row in self.tree.get_children():
            self.tree.delete(row) #Clear any previous rows in the Treeview
        if tasks is None:  #If no specific task list is passed, use all tasks from the task manager
            tasks = self.task_manager.tasks
        for task in tasks: #Insert each task into the Treeview (like adding rows to a table)
            self.tree.insert("", tk.END, values=(task.name, task.description, task.priority, task.due_date))
    
    def apply_filter(self):
        name = self.name_entry.get()   # Get filter inputs from user
        priority = self.priority_var.get()
        due_date = self.date_entry.get()
        filtered_tasks = self.task_manager.get_filtered_tasks(name, priority, due_date)   # Get filtered tasks from task manager
        self.populate_tree(filtered_tasks)  # Update the Treeview with only filtered tasks
        
    def sort_tasks(self, column):
        key_map = {"Name": "name", "Description": "description", "Priority": "priority", "Due Date": "due_date"}
        sort_key = key_map[column]  # Get the attribute name for sorting
        self.task_manager.sort_tasks(sort_key)  # Sort tasks using the task manager's sorting method
        self.populate_tree()  # Refresh the Treeview with the sorted tasks

# Main program
if __name__ == "__main__":
    root = tk.Tk()  #create the main window
    app = TaskManagerGUI(root) # Create an instance of your app
    root.mainloop() #runs the app without closing
