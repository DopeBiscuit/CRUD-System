# CRUD System
#### Video Demo:  <https://youtu.be/43bIVBGfvCw>
#### Description:

**I will start by description of the how the site looks and how to navigate it, and also discussing its functionality, after this I will explain what each file contains in the end of this file.**

Hello, so first all the concept, the **CRUD** System in spirit was supposed to be similar to *Excel* or *Google Sheets*, where users could log on to the site and create their databases,
where in each database the user could have a number of tables to their desire, while creating each table the user will be able to select the number of columns and even their datatypes, the project was created using Flask, HTML, CSS, SQL, Javascript and Jinja.

---

### **Upcoming explanation is provided in the video linked above.**

---
<img src="/Images/Log in.png"><br>
**First** of all the user is prompted with the log in page, the user has to enter the credentials of their account if one does exist, incorrect credentials will prompt the user with an alert explaining what criterion was not met.

**If** the user doesn't already have an account they will need to register an account, to access the register page the user just simply clicks on the **Register** Link below the **Log In** button.

---

<img src="/Images/Register.png"><br>

**Register** page is then rendered for the user, the user now has to input all of the required fields to create a valid account, there are certain criteria that must be met, failing to meet any of them will result in an alert explaining what criterion wasn't met.

Criteria:
- All data fields are populated
- Uniqueness of Username
- Password is at least 8 characters long
- Password and the confirmation match

<img src="/Images/HomePage.png"><br>
**After** the user successfully logs in or register an account, they are redirected to the homepage, the homepage is where all the databases of user are available, and where the user can create or delete databases, the page consists of small form, the select menu automatically populates with all the available databases of the user, to access the database click on it from the select menu and hit the select button. 

**For** a fresh account there will be no databases, therefore no options to select from in the select menu, to create a database hit the green create button, if a user wants to delete an existing database simply hit the red delete button.

---
<img src="/Images/CreateDB.png"><br>
**The** user will then proceed to insert the desired name and press create, the user must enter a name or they will be prompted with an alert, the database name must be different from already existing databases for the user.

**If** the user decides not to create a database and wants to back to the homepage, simply click on the home button in the **Navbar** in the top left corner.

---
<img src="/Images/DeleteDB.png"><br>
<div style="text-align: justify; text-justify: inter-word;">
<b>If</b> a user does prefer to delete a database, after clicking the red delete button from the homepage, the user will be redirected to the delete page for extra caution, the user now will select the database they want to erase from the select menu then hit delete database, the user will then be redirected to the homepage. 
</div>

**Caution: *Deleted data can not be restored.***

**If** the user decides not to create a database and wants to back to the homepage, simply click on the home button in the **Navbar** in the top left corner.

---
<img src="/Images/EditDB.png"><br>
 After the user selects a database from the homepage they will be redirected to the edit database page, this is where the data handling will happen, the user can select in similar fashion a table from the selected database to edit, the user can also delete an existing table, or create a new table.

---
<img src="/Images/CreateTB.png"><br>
<div style="text-align: justify; text-justify: inter-word;">
If the user clicks the <b>Create Table</b> button they will be redirected to the table creation page, the page will include a simple form requiring the name and the number of columns of the table.
<br><br>
<b>Table Name must not start with a number. </b>
<br><br>
<b>After</b> the user inputs the number of columns required and hit <b>Load</b> button, the page is automatically updated with new inputs for column name and datatype equal to the number of desired columns.
<br><br>
<b>All input fields are mandatory.</b>
<br><br>
<b>The</b> user will begin filling the columns' info, <b>Column name must not start with a number</b>, and if no exact datatype is selected then the datatype will be defaulted to text.
</div>

---
<img src="/Images/DeleteTB.png"><br>
<div style="text-align: justify; text-justify: inter-word;">
<b>If</b> the user clicked on the <b>Delete Table</b> button they will be redirected to the delete table page, the user will proceed to select the table they want to delete from the select menu and hit Delete.
<br><br>
<b>Deleted Data can not be restored</b>
<br><br>
<b>After</b> hitting Delete the user is redirected to the edit database page again.
</div>

---
<img src="/Images/table.png"><br>
<div style="text-align: justify; text-justify: inter-word;">
<b>In</b> the edit database page, you can select the table you want to edit, after clicking the  <b>Select</b> button the table is automatically loaded into the page, all freshly created tables will have an empty first row.
<br><br>
<b>The</b> user can edit rows by inserting the wanted values in each data field and then clicking the blue button with the pencil icon on it, <b>(Edit)</b>.
<br><br>
<b>The</b> user can delete a row by clicking the red button with the trash icon on it. <b>(Delete)</b>
<br><br>
<b>Only one row can be Deleted/Edited at a time.</b>
<br><br>
<b>The</b> user can create a new row by inserting the wanted data in the last row then clicking the greed button with the plus on it <b>(Add)</b>, if no data is given in the fields the newly added row is set to be blank.
<br><br>
<b><i>Clicking the Select button without choosing a table will result in unloading the current active table.</i></b>

</div>

---
<img src="/Images/DatabaseMenu.png"><br>
<div style="text-align: justify; text-justify: inter-word;">
<b>If</b> the user wants to select another database to edit it, they can click the home button in the top left of the <b>Navigation Bar</b> to go to the homepage, or they could use the database menu also found in the <b>Navigation Bar</b> in the top left of the screen, where all databases for the current user are displayed, click the desired database to activate and start editing it.
</div>

---

**The user can click the Log out in the top right of the screen to log out of the current account.**

---

**And this is basically it, the tabular data management system, the user can create an account, make their own databases, delete them, or edit them, with in each database the user can create their tables and edit them or delete them if they want.**

### So what do the files in the final project include:
- **app.py**, basically the main file, where all the logic is applied, deals with all GET and POST requests, including all the redirects and functions
- **helpers.py**, used for the require log in functionality.
- **main.db** this is the main database where it includes 2 tables, the users table that stores the user's unique autoincrementing ID, username and hash of their password, and also include the ref table, which includes the ID's of the users and their respective databases.

- **static folder**, it includes the css file that is the same file from the cs50 finance problem set for the nav bar css
- **requirements.txt**, includes the required python packages in this project.
- **layout.html**, includes the layout of the nav bar and the page background
- **apology.html**, contains the apology that appears in case of errors.
- **createdb.html and createtb.html**, includes the html for the creation pages, where the createtb uses javascripts to change the html of the page to load the required amount of input field pairs.

- **index.html**, html of the main page where the user selects the database required to navigate.
- **deletedb.html and deletetb.html**, include the html for the deletion pages, uses jinja and javascript to auto populate the select fields with the available tables or databases.

- **login.html and register.html**, include the html for the the log in and register page

- **editdb.html**, includes html of the page where the user will select a table to edit, where the page uses jinja and html to display the tables in the select field and also to change the page's html to view the table once selected by the user and edit the table's content

---

#### **Special thanks to the following contributors for their help with ui adjustments and bug fixing:**
- M7MD <mohamed040406@users.noreply.github.com>
- Omar Attia <OmarMAttia7@users.noreply.github.com> 

