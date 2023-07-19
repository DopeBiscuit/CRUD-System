# CRUD System
#### Video Demo:  <https://youtu.be/Kxe2LDVBDQo>
#### Description:

**I will start by description of the how the site looks and how to navigate it, and also discussing its functionality, after this I will explain what each file contains in the end of this file.**

Hello, so first all the concept, the crud system in spirit was supposed to be similar to excel or google sheets, where users could log on to the site and create their databases,
where in each database the user could have a number of tables to their desire, while creating each table the user will be able to select the number of columns and even their datatypes, the project was created using Flask, html, css, javascript and Jinja.

**So** let's get started by the first thing the user will be prompted with when they opens the website, they will automatically be directed to the log in page, in which the user will have to insert valid username and password saved in the system.

**If** the user doesn't enter a username or a password they will be redirected to an apology page used from the cs50 finance problem set the user can then get back to the previous page by clicking back button in their browser or clicking on the "CRUD System" logo in the top left of the nave bar where they will be redirect to the main page if they are logged in.

**Some** of the css as well is reused from that probelm set as apparent, in the backend using python and sqlite3 I make sure that the user inputed data in both fields, after that using logic match those inputs to the rows in my users table in my main.db to see if credentials do actually exist, of course after hashing the password of the user, after the user logs in he will be redirected to the homepage.

**If** the user doesn't already have an account they will need to register by clicking register on the top right of the nav bar, after which they will be redirect to the register page, The user then will be prompted with 3 text fields where they input desired username and the password and password confirmation to make sure user inputed correct password,

**Snippets** of codes for registeration and log in are reused from the cs50 finance problem set,after the user inputs the **3** fields, i make sure that they actually did that in the back end, and make sure that both password and its confirmation **do match** indeed, also make sure that the username doesn't already exist in my users table, for each problem in these they will be redirected to an apology page, where each error gets its own apology, if no errors exist then I insert a new row in the users table with user's new username and hash of their password, and then the user get's assigned a session Id equal to the autoincrementing ID in the users table and autoredirected to the homepage.

**After** the log in or registers and is transfered to the homepage, they will be presented with a select field a button and **2 links**, first the select field, where all current available databases of the current user will be displayed, if user doesn't have any then they will have to click the "Create Database" link in the top left of the page, Where they will be redirected to the database creation page, on the page they will be presented by a Text field and a create button.

**The** user will then proceed to insert the desired name and press create, if the user doesn't enter a name and presses create they will be redirected to an error page, the way a database is created is by using open file in write mode in the main directory with the name inserted by the user preceded by the user's id, so that even if 2 or more users pick the same name for their databases, it will alwasy be unique, now once the user click create, the .db file will be created and then the user will be redirected again to the homepage, where they once again could select a database, create or even delete one.

**If** a user does prefer to delete a database, they will click the link and be redirected to the delete database page, where the user will be prompted by a select field and a delete button, inside the select field using jinja and javascript all available databases for the user will appear, they can then proceed to select one and click delete, if they don't select one though, the user will be redirected to an apology page for not selecting a database, when a user does select a database, said database will be removed by **os.remove** in the backend, and then the user will be redirect back to the homepage, if the user of course clicks Select without actually selecting a database, they will be redirected to an apology page for not selecting a database, if the user does select a database and then click select they will be redirected to the edit database page.

**Where** most of their data manipulation will occur, first of all the user will be presented with extremely simliar page to the homepage, where the user will have the ability to create, delete or select a table within the selected database.
If the user click the create table link in the top right of the page, they will be redirected to the table creation page, the page will include a text field at the very top which requires the table name, on condition that the first character must be a character due to sqlite3 limitations, if user inserts first character not a letter, then they will be redirected to an apology page,

**If** the table name includes space characters, it will automatically be replace by **"_"** character due to sqlite3 limitations, after the name is provided the user will then proceed to a number field where the user will input the desired number of columns for their table, the default is one, the number must be equal to or greater to one, if it isn't the user will recieve a browser alert using javascript saying must be greater than zero, after the user inputs the number of desired columns, they will click on load, which triggers a javascript event that loads up pairs of text fields with select fields, a number of pairs equal to the column number will appear on the screen, where the text field will be required and will take the name of the column in order, the first field being the first column, and the select field will contain the available datatypes in sqlite3.

**The** user will then proceed to insert a name for each column and a datatype,
since the name field is required the user will have to insert a value, and if the user doesn't insert a datatype for the column it will automatically be made text in the backend, by matching up every text field to its representative datatype select field using python, the column name must start with a letter as well, or the user will get an apology, if the user inputs all fields and then clicks create, the backend will concatenate the strings of values from the input fields to create a sqlite3 command that will create the desired table within the selected database, and then the user will be redirected to the edit database page.

**If** the user then wants to delete a table, they will click on the delete table in the top right of the page, where they will be redirected to the delete table page, the page will inclue a select field and a delete button similar to the delete database page, the user will then proceed to select a table from their availabe tables from the select field, if the user doesn't pick one and clicks delete they will recieve an apology, if they select one and then press delete, in the backend a command is executed to delete picked table from the active database, and the user will be redirected to the edit database page again.

**In** the edit database page the select field will contain all availabe tables in the selected databse, if the user doesn't select one and click the select button they will recieve an apology, if the user selects a table and clicks select, the page will be updated to include a dynamic table portraying the data within the selected table if it exists, the javascrip created table is dynamic as it changes size depending on the size of the selected table, the user can also still use the select field to change the selected table to another one, where the page will be updated with the new table,

**With** in the table, newly created tables will always have a null row with no values, under each column in the table there will be an input field with its value equal to the value in the sql table if it exists, in the case of null row its blank, besides each row the right there will be two buttons a delete and an edit button,
if the user wishes to delete a certain row all they have to do is click that row's delete button which then will execute a sql command that will delete that row from the table, unless the table has only 1 row where the user will then be redirected to an apology that each table must at least have one row due to logic purposes,
as all tables are created with a secret column not viewable to the user called secret_id where its a primary key that autoincrements, and is used for row refrencing in the back end,

**Now** if the user wishes to edit data with in the table they will have to do it row by row due to the design of the logic, the user will first input the values within the input fields in desired row and the proceeds to click on the edit button related to that row, where the page will be quickly reloaded and the data will be saved to the table, where the query was executed in the backend, if the user edits the values of 2 or more rows and the clicks the edit button of one row of them all changed data in other rows will be reverted due to the desing of the logic, so will this happen if the user click delete to a row.

**You** will notice that each column's input field is bounded by the datatype the user specified, where integer generates a number field, and numeric and real generates a number text that accepts decimals, and text and blob acceptes text,
In all tables the last row rendered will always be a new blank row that isn't actually with in the table, this row will have an add button next to it, the user can insert the required data they want and then click add where this row will be appended to the table, and a new add row will be render for if the user wants to add another row, all these features are availabe on all tables in all databases, the user can use the select field at the top of the page to switch between tables in the database.

**If** the user wishes they could use the log out in the top right of the nav bar after they have logged in if they want to log out, where they will have to log in again if they wish to access their data.

**And this is basically it, the tabular data management system, the user can create an account, make their own databases, delete them, or edit them, with in each database the user can create their tables and edit them or delete them if they want.**

### So what do the files in the final project include:
- **app.py**, basically the main file, where all the logic is applied, deals with all GET and POST requests, including all the redirects and functions
- **helpers.py**, this is an edited file from the cs50 finanace problem set, used to for the apology functionality and the require log in functionality.
- **main.db** this is the main database where it includes 2 tables, the users table that stores the user's unique autoincrementing ID, username and hash of their password, and also include the ref table, which includes the ID's of the users and their respective databases.

- **static folder**, it includes the css file that is the same file from the cs50 finance problem set for the nav bar css
- **requirements.txt**, includes the required python packages in this project.
- **layout.html**, includes the layout of the nav bar and the page background
- **apology.html**, contains the apology that appears in case of errors.
- **createdb.html and createtb.html**, includes the html for the creation pages, where the createtb uses javascripts to change the html of the page to load the required amount of input field pairs.

- **index.html**, html of the main pagae where the user selects the database required to navigate
- **deletedb.html and deletetb.html**, include the html for the deletion pages, uses jinja and javascript to auto populate the select fields with the available tables or databases.

- **login.html and register.html**, include the html for the the log in and register page

- **editdb.html**, includes html of the page where the user will select a table to edit, where the page uses jinja and html to display the tables in the select field and also to change the page's html to view the table once selected by the user and edit the table's content