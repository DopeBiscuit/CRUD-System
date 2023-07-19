#from crypt import methods
import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///main.db")
udb = 0


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    # Check for request method.
    if request.method == "POST":
        # Ensure user selected a database
        if not request.form.get("databases"):
            return apology("Must pick a database.", 400)

        # Get Selected Database then call it as a global variable for future reference.
        dbname = str(session["user_id"]) + request.form.get("databases") + ".db"
        global udb
        udb = SQL(f"sqlite:///{dbname}")
        return redirect("/editdb")

    else:
        # Load up users's databases.
        user_dbs =  db.execute("SELECT dbname FROM ref WHERE id = ? ORDER BY dbname", session["user_id"])
        return render_template("index.html", user_dbs=user_dbs)

@app.route("/createdb", methods=["GET", "POST"])
@login_required
def createdb():
    """Makes a new database for a user."""
    # Check for request method.
    if request.method == "POST":
        # Ensure user gave a database name.
        if not request.form.get("dbname"):
            return apology("Must enter database name.", 400)

        # Get database name.
        dbname = request.form.get("dbname").lower()

        #Ensure no user has same name for their database.
        dbs = db.execute("SELECT dbname FROM ref WHERE dbname = ?", dbname)
        if dbs:
            return apology("Database name not available", 400)

        # Create database file in main directory
        f = open(str(session["user_id"]) + dbname + ".db", 'w')
        f.close()

        # Insert new database name with user id in the ref table in main database.
        db.execute("INSERT INTO ref (id, dbname) VALUES (?, ?)",
                   session["user_id"], dbname)

        return redirect("/")
    else:
        return render_template("createdb.html")


@app.route("/editdb", methods=["GET", "POST"])
@login_required
def editdb():
    """Edit database,"""
    # Ensure user submitted data
    if request.method == "POST":
        if not request.form.get("tables"):
            return apology("Must select table", 400)

        table = request.form.get("tables")

        # Load data to send to site
        tbnames = udb.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_sequence' ORDER BY name")
        data = udb.execute("SELECT * FROM ?", table)
        dtypes = udb.execute("SELECT type from pragma_table_info(?) as tblInfo;", table)
        keys = list(data[0].keys())
        row_len = len(keys)
        data_len = len(data)
        return render_template("editdb.html", data=data, keys=keys, row_len=row_len, data_len=data_len, table=table, tbnames=tbnames, dtypes=dtypes)
    else:
        tbnames = udb.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_sequence' ORDER BY name")
        data = []
        keys = []
        dtypes = []
        row_len = len(keys)
        data_len = len(data)
        return render_template("editdb.html", tbnames=tbnames, data=data, keys=keys, row_len=row_len, data_len=data_len, dtypes=dtypes)

@app.route("/createtb", methods=["GET", "POST"])
@login_required
def createtb():
    """Makes a new table for a user."""
    # Check for request method.
    if request.method == "POST":
        # Ensure user gave a table name.
        if not request.form.get("tbname"):
            return apology("Must enter database name.", 400)

        # Ensure first letter is alphabetic
        tbname = request.form.get("tbname").lower().replace(' ', '_')
        if not tbname[0].isalpha():
            return apology("First character of the table name must be an alphabetic character.", 403)

        # Get table name and check availability.
        tbnames = udb.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ? ORDER BY name", tbname)
        if tbnames:
            return apology("Name already in use.", 400)

        # Loop through user's input to make table
        clm_num = int(request.form.get("num-clm"))
        table_command = "CREATE TABLE " + tbname + " (secret_id INTEGER PRIMARY KEY AUTOINCREMENT, "
        first_row = "INSERT INTO " + "'" + tbname + "'" + " ("

        for i in range(clm_num):
            # Ittirative vars
            txtc = "txt" + str(i)
            dtype = "datatype" + str(i)

            # Get current column and datatytpe
            clm_name = request.form.get(txtc)
            data_type = request.form.get(dtype)

            if not clm_name[0].isalpha():
                return apology("First character of column name must be an alphabetic character.")

            if not data_type:
                data_type = 'TEXT'

            # If first ittiration, then don't add comma to the start, if not then add, and then add column name followed by space and datatype.
            if i == 0:
                table_command = table_command + clm_name + " " + data_type
                first_row = first_row + clm_name
            else:
                table_command = table_command + ", " + clm_name + " " + data_type
                first_row = first_row + ", " + clm_name

        # Close string to be able to execute it.
        first_row = first_row + ") VALUES ("
        for i in range(clm_num):
            if i == 0:
                first_row = first_row + '""'
            else:
                first_row = first_row + ', ""'

        first_row = first_row + ");"
        table_command = table_command + ");"

        # Create table
        udb.execute(table_command)
        udb.execute(first_row)

        return redirect("/editdb")
    else:
        datatypes = ["TEXT", "INTEGER", "REAL", "NUMERIC", "BLOB"]
        return render_template("createtb.html", datatypes=datatypes)

@app.route("/delrow", methods=["POST"])
@login_required
def delrow():
    # Get value of pressed button to get secret_id.
    btn_val = request.form.get("delbtn").split()
    ID = btn_val[0]
    name = btn_val[1]
    data = udb.execute("SELECT * FROM ?", name)

    if len(data) == 1:
        return apology("Cant delete all rows, would you like to drop table instead ?", 400)
    # Delete row from table
    udb.execute("DELETE FROM ? WHERE secret_id = ?", name,ID)
    data = udb.execute("SELECT * FROM ?", name)
    tbnames = udb.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_sequence' ORDER BY name")
    dtypes = udb.execute("SELECT type from pragma_table_info(?) as tblInfo;", name)
    keys = list(data[0].keys())
    row_len = len(keys)
    data_len = len(data)
    return render_template("editdb.html", data=data, keys=keys, row_len=row_len, data_len=data_len, table=name, tbnames=tbnames, dtypes=dtypes)




@app.route("/editrow", methods=["POST"])
@login_required
def editrow():
    # Get values of rows to be editited
    btn_val = request.form.get("editbtn").split()
    ID = btn_val[0]
    tbname = btn_val[1]

    # Get a list of columns of the selected table
    columns = udb.execute("SELECT name from pragma_table_info(?) as tblInfo;", tbname)
    # Start piecing together the string that will be the query command
    cmnd = 'UPDATE ' + tbname + ' SET '

    # Loop through the columns while also getting the values from the text field.
    for i in range(1,len(columns)):
        txtc = 'txt' + str(i)
        if i == (len(columns) - 1):
            cmnd += columns[i]["name"] + ' = "' + request.form.get(txtc) + '" '
        else:
            cmnd += columns[i]["name"] + ' = "' + request.form.get(txtc) + '", '

    # Finish up the cmnd string and then execute the query.
    cmnd += 'WHERE secret_id = ' + ID
    udb.execute(cmnd)

    # Query all required data again to render editdb page.
    data = udb.execute("SELECT * FROM ?", tbname)
    tbnames = udb.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_sequence' ORDER BY name")
    dtypes = udb.execute("SELECT type from pragma_table_info(?) as tblInfo;", tbname)
    keys = list(data[0].keys())
    row_len = len(keys)
    data_len = len(data)
    return render_template("editdb.html", data=data, keys=keys, row_len=row_len, data_len=data_len, table=tbname, tbnames=tbnames, dtypes=dtypes)


@app.route("/addrow", methods=["POST"])
@login_required
def addrow():
    # Get values of row to be added
    tbname = request.form.get("addbtn")


    # Get a list of columns of the selected table
    columns = udb.execute("SELECT name from pragma_table_info(?) as tblInfo;", tbname)
    # Start piecing together the string that will be the query command
    cmnd = 'INSERT INTO ' + tbname + ' ('
    vals = '('

    # Loop through columns piecing together the cmnd string for the insertion
    for i in range(1,len(columns)):
        txtc = 'txt' + str(i)
        if i == (len(columns) - 1):
            cmnd += columns[i]["name"] + ') VALUES '
            vals += '"' + request.form.get(txtc) + '")'
        else:
            cmnd += columns[i]["name"] + ', '
            vals += '"' + request.form.get(txtc) + '", '

    # Finish up the cmnd string then execute the qeury
    cmnd = cmnd + vals
    udb.execute(cmnd)

    # Query required data to re render the editdb page.
    data = udb.execute("SELECT * FROM ?", tbname)
    tbnames = udb.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_sequence' ORDER BY name")
    dtypes = udb.execute("SELECT type from pragma_table_info(?) as tblInfo;", tbname)
    keys = list(data[0].keys())
    row_len = len(keys)
    data_len = len(data)
    return render_template("editdb.html", data=data, keys=keys, row_len=row_len, data_len=data_len, table=tbname, tbnames=tbnames, dtypes=dtypes)


@app.route("/deletetb", methods=["GET", "POST"])
@login_required
def deletetb():
    if request.method == "POST":
        if not request.form.get("tables"):
            return apology("Must select table", 400)

        table = request.form.get("tables")
        udb.execute("DROP TABLE ?", table)

        # Return to editdb
        return redirect("/editdb")
    else:
        tbnames = udb.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_sequence' ORDER BY name")
        return render_template("deletetb.html", tbnames=tbnames)


@app.route("/deletedb", methods=["GET", "POST"])
@login_required
def deletedb():
    # Check for request method.
    if request.method == "POST":
        # Ensure user selected a database
        if not request.form.get("databases"):
            return apology("Must pick a database.", 400)

        # Delete selected database
        dbname = str(session["user_id"]) + request.form.get("databases") + ".db"
        dbn = request.form.get("databases")
        os.remove(f"{dbname}")
        # Remove database from ref table in main database
        db.execute("DELETE FROM ref WHERE dbname = ?", dbn)

        return redirect("/")
    else:
        # Load up users's databases.
        user_dbs =  db.execute("SELECT dbname FROM ref WHERE id = ? ORDER BY dbname", session["user_id"])
        return render_template("deletedb.html", user_dbs=user_dbs)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # If request method is post, meaning user has submitted registeration creditnetials.
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        username = request.form.get("username")

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Ensure password matches password confirmation.
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password and password confirmation must match", 400)
        password = request.form.get("password")

        # Query database for usernames to make sure it is unique.
        usernames = db.execute("SELECT username FROM users WHERE username = ? ", username)

        # Ensure username doesn't exist
        if len(usernames) != 0:
            return apology("Username already exists.", 400)

        # If all checks are green, then insert new row into users table in database with new data.
        db.execute("INSERT INTO users (username,hash) VALUES (?,?)", username, generate_password_hash(password))

        # Give session to remember sign in
        ID = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = ID[0]["id"]

        # Redirect to homepage
        return redirect("/")

    else:
        return render_template("register.html")

