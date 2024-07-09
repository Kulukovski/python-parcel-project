# python-parcel-project
Parcel Hive Project
Create an application that uses parallel processes / multiprocessing via python using a browser environment to visualize the current reading of serial data from the movement of the mouse and when the left mouse’s button is pressed take a picture of a connected webcam. As a final result, to save the current coordinates of the mouse cursor and data-source of the image in sqllite database.

Basic modules and stages for evaluation during implementation

1. Asyncio

2. Webserver

3. Websockets

4. Pyserial

5. OpenCV

6. SQLite/DBmongo

There are three core python scripts in this project: server, dbcontrol and sqldb

1. server is the script that controls the connection with the server which includes the data transfer of the mouse location and mouse clicks. After it collects that data, it initializes the webcam and commits that data to a database which stores the directory path of the image, as well as the x and y coordinates of the mouse.

2. dbcontrol is used to interface with the database. Things such as listing elements, deleting elements and verification of the database elements against the directory files.

3. sqldb is the script which houses all of the functions necessary for interfacing with the images database. It was structured this way to eliminate the need for repeating functions between the first 2 scripts, making the code more concise and the database simpler to interface with regardless of where we do it from.

   Additional files:
   
1. index.html is the html file which holds the website code as well as javascript necessary for the collection  of mouse data which passes it to the server.py script.

2. images.db is the database which holds the infomation about the image paths as well as the x and y coordinate at which the image was taken.

To run the project: 

Start the server.py script and launch [localhost:8000](http://localhost:8000/), this website is where you can move the mouse and the script will visualize the coordinates as well as when left click is pressed. When left click is pressed the webcam takes a picture and saves it to the database. The database data can be retrived and manipulated in dbcontrol.py using the functions from sqldb.py.
