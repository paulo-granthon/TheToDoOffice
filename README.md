# To Do Office

A place where you can easily manage your tasks. Create, track, complete and organize tasks between folders with fast and simple inputs

## 🤔 What is it?
ToDoOffice is a web based application made predominantly with Django and HTMX that allows the user to create and keep track of *Tasks* and complete them with a single click.

## ✍ How to use
### 📄 Create Tasks:
> Just **type** it's name or text into the *input box on the top left corner* and click *Add* or press *Enter* on your keyboard to create a Task. It will be created inside the *currently opened* ***Folder*** OR on the *root* folder of your account if no Folder is selected.

### ✔️ Complete Tasks:
> On the left side of a Task, click the *checkbox* to check or uncheck the completion status of that Task.  

### 🌠 Move Task:
> On the right side of a Task, when you hover your mouse over it, the *move* button will be revealed. *Click* it to show a pop-up with a list of Folders. Select which on you want to move the Task to. A confirmation dialog will appear with the options to confirm or cancel.  

### ❌ Delete Task:
> On the right side of a Task, when you hover your mouse over it, the delete button will be revealed. *Click* it to show a pop-up with a confirmation to delete the Task.  

### 🌟 Select Tasks:
> when you click over the *body* of a Task, the Task will be selected. Currently there are no actions that you can do using the selected Task(s), however, there are planned functionalities that will put this resource to a good use in a near future.

> #### **Select multiple Tasks:**
> > You can have **multiple** Tasks selected by *selecting a task while pressing the* ***ctrl key*** *on the keyboard*.

### 💼 Create Folders:
> Click the *New Folder* button on the top right corner of the *Folder List*, just bellow the *input box*. A pop-up will appear, type the Folder's name and click *Ok* or press *Enter* to finish creating the Folder.  

### 📁 Open Folder:
> The *Folder List* will display all you Folders, just *click* one of them and it will open, revealing it's Tasks on the right side of the screen. 

### ❌ Delete Folder:
> On the *Folder List*, whenever you hover your mouse pointer over a Folder, the delete button will be revealed. *Click* it to show a pop-up with a confirmation to delete the Folder.  

## 📱 Goals
#### General
> - [x] Light/Dark themes.  
#### Authentication:
> - [x] Register and login.  
#### Tasks:
> - [x] Create and delete.
> - [x] Check as completed.
> - [x] Move to/from Folder.

> - [x] Select one or more Task(s)

> - [ ] Reorder.
> - [ ] Drag & Drop actions.  
#### Folders:
> - [x] Create and delete.
> - [x] Open and display it's contents.
> - [ ] ~~Nested Folders.~~

## 📜 Technologies Used
- Django (Python)
- HTMX (+ HyperScript)
- JavaScript
- HTML & CSS
