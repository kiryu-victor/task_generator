## What is this?
**This is a WIP project** consisting of a task manager for three milling machines, each one with some materials that each machine can work with, which operate within a range of speeds measured in SMM *(Surface Meters per Minute)*.
> [!NOTE]
> Bear in mind that for the purpose of this project the data is not realistic and it is very simplified. This way each operation is easily understandable for the purpose of learning.



## How does it work?
- The first window that appears is the one with the details of all the tasks. This can be sorted by column if the user wants to.
  - It shows: ID (based on datetime), creation time, machine, material, speed, status
    - The "status" column can have the next values:
      - "On queue" for tasks that are yet to start.
      - A countdown to 0 when it is a ongoing task.
      - "Completed" for tasks that have finished.
- The "Create" button pops a modal window asking for machine, material and speed.
  - The user has to fill the fields in that order because each machine has different material that it can work with.
  - Those materials operate at certain speeds, that are checked in order to create the tasks successfuly.
- The "Modify" button pops a modal window with the same fields, but it also shows a column with the old parameters for reference.
  - "On queue" tasks can be modified completely (machine, material and speed).
  - Ongoing tasks that have started can only have its speed modified.
  - "Completed" tasks cannot be modified at all.
- The "Delete" button does exactly that.
  - It opens a menu for confirmation before deletion.
- The SQLite database (tasks.db) has three entries in the current state: one with each possible status so you can try different operations with them.



## How is it made?
#### Tech used:
Python, venv, tkinter, ~~CSV~~, SQLite, asyncio, websockets

#### TLDR:
 1. Task are loaded from DB on app start.
 2. TaskManager loads the data.
 3. The main view displays said data on a table.
 4. User can create tasks or modify/delete a selected task (depending on status) by clicking on the buttons at the bottom.
 5. On the click of any of those buttons, a new view (or error message) opens.
 6. User inserts the inputs in order, which are validated.
 7. Once the operation is done the tasks are loaded again, populating the table.

<ins>**OLD:**</ins>
> The TaskManager (model) class loads the CSV file with all the tasks.
It handles creation, modification and deletion operations, saving them back to the CSV file. Until then, the tasks are stored in memory as a list of dictionaries they are sorted into machine-specific queues. It was made like this because it was going to be only one client.

<ins>**NEW:**</ins>
> The TaskManager (model) loads the data from the DB (tasks.db). It handles creation, modification and deletion operations.
It handles creation, modification and deletion operations on the database (DB). With each operation, the view updates with the current data of the DB.
> Visible countdown is triggered by the server when a new task is created, modified or deleted. Every other time, clients refresh the tasks' "Time left" by themselves, freeing server work.
<ins>**COMMON**</ins>
tkinter is used for the views (GUI). The MainView is the main window with all the tasks, and then each operation has its own class. The GUIs have buttons that let the user create, modify and delete tasks.
The controllers (MainController, CreateTaskcontroller...) deal with the inputs, validate data and update the model and view.
Utils is a folder that has utils.py, that serves to center the app on the screen and validate inputs, and config.json, that has the different machines, materials, speed ranges and ETCs that are used on the inputs.



## But... why?

This project is the one that is gathering most of the things that I've learned by myself.
I have been programming on Java since I started my regulated/certified studies, but I want to try Python and explore the posibilities it has. With this I'm learning:

- Python
- Pythonic coding. A new concept to me that I'm trying to follow.
- PEP8 and PEP9. Another thing I didn't know about but got told about recently.
- tkinter
- SQLite
- asyncio
- WebSocket updates 



## To-do list

- [x] "Delete" should work only on "On queue" and ongoing tasks.
  - [x] "On queue": no issue.
  - [x] Ongoing:
    - [x] Countdown logic has to be implemented.
    - [x] Countdown reaching 0 logic.
    ~~- [ ] Ongoing task modification or deletion pauses the task until finishing or canceling the operation.~~
    - [x] Ongoing task deletion logic, triggering the next on the list to start.
- [ ] Time left is based on the machining surface.
  - [ ] Implement size_max and size_min configuration for a piece.
  - [ ] Randomize the actual size.
  - [ ] Base the time left on the speed.
  - [ ] On modification of the speed, the time left changes too.
> [!NOTE]
> Deleted the countdown because it won't be used that way when implementing WebSockets (or so I think).
- [x] Migrate to SQLite.
- [x] Implement WebSocket-based updates.
- [x] Limited DB queries to the WebSocket server alone.
- [ ] Make different status easier to be seen changing the background of the rows:
  - [ ] Green: "Completed"
  - [ ] Blue: "On queue"
  - [ ] ...
- [ ] Add filters to every column (not only sorting).
- [x] Make it all prettier.
  - It became part of the regular list after many testing tries.
  - [x] Start with darker colours:
    - GUI is way too bright.
    - Switching between dark themed everything else and this bright themed GUI hurts.
  - [x] Adjusted colour and style to fit better.
