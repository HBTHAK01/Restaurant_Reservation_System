from dns.rdatatype import NULL
from flask import Flask, render_template, url_for, request, flash, redirect, session
from flask_session import Session
import mysql.connector
from werkzeug.utils import redirect
import datetime


app = Flask(__name__)


"""
SQL One Time Code Till Now


1.
'CREATE DATABASE Restaurant_Reservation'

2.
'''CREATE TABLE Users (
First_Name VARCHAR(255), 
Last_Name VARCHAR(255),
Phone_Number VARCHAR(255),
Email VARCHAR(255),
Password VARCHAR(255)
)'''

3.
'''ALTER TABLE Users
MODIFY First_Name VARCHAR(255) NOT NULL,
MODIFY Last_Name VARCHAR(255) NOT NULL,
MODIFY Phone_Number VARCHAR(255) NOT NULL,
MODIFY Email VARCHAR(255) NOT NULL,
MODIFY Password VARCHAR(255) NOT NULL;

ALTER TABLE Users
ADD PRIMARY KEY (Email)'''

4.
'''CREATE TABLE Bookings (
Table_Name VARCHAR(255),
Capacity VARCHAR(255),
Name VARCHAR(255), 
Phone VARCHAR(255),
Email VARCHAR(255),
Date VARCHAR(255),
Time VARCHAR(255),
Booked BOOL
)'''

5.
'''INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 1", "2")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 2", "2")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 3", "2")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 4", "2")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 5", "2")

INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 6", "4")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 7", "4")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 8", "4")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 9", "4")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 10", "4")

INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 11", "6")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 12", "6")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 13", "6")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 14", "6")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 15", "6")

INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 16", "8")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 17", "8")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 18", "8")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 19", "8")
INSERT INTO Bookings (Table_Name, Capacity) VALUES ("Table 20", "8")
'''

6.
'''ALTER TABLE Bookings
ADD PRIMARY KEY (Table_Name)
'''

7.
'''
UPDATE Bookings
SET Booked = 0
'''

8.


"""








#add
app.config["SESSION_PERMANENT"] =  False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
#end add

app.secret_key = "abc"  

# Database Part for MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="",
  password="",
  database="Restaurant_Reservation"
)


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        email_login = request.form['email_login']
        pass_login = request.form['pass_login']  
              
        mycursor = mydb.cursor()
        # sql_select = "SELECT Email, Password FROM Users"
        # mycursor.execute(sql_select) 
        # result = mycursor.fetchall()

        # session["email"] = email_login #get email to html 
        mycursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email_login, pass_login, ))
        account = mycursor.fetchone()
        # print(account)

        if account:
            # session['name'] = account['name']
            session['name'] = account[0] #change tuple

            return redirect ("/user_reservation")
        else:
           flash("Email and/or password is incorrect.", "error")

        # print(result)
        # for i in range(len(result)):
        #     if email_login == result[i][0] and pass_login == result[i][1]:
        #         # mycursor.execute('Select First_Name from users where Email = %s', (email_login))
        #         # msg = mycursor.fetchone()
        #         session["name"] = "HELLO"
        #         return redirect ("/user_reservation")
        #     else:
        #         flash("Email and/or password is incorrect.", "error")


    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM bookings WHERE Booked = %s', (1,))
    bookings_ = mycursor.fetchall()
    # print(bookings_)

    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")
    # print(now_date)
    now_time = now.strftime("%H:%M:%S")
    # print(now_time)

    for i in bookings_:
        if now_date == i[5]:
            # print("yes")
            current = datetime.datetime.strptime(now_time,"%H:%M:%S")
            entry = datetime.datetime.strptime(i[6],"%H:%M")
            time_interval = current - entry
            # print(time_interval)
            if time_interval > datetime.timedelta(hours= 1 , minutes=00, seconds=0):
                # print("Yes Sir")
                sql_update = """UPDATE Bookings 
                        SET Name = NULL, Phone = NULL, Email = NULL, Date = NULL, Time = NULL, Booked = %s
                        WHERE Table_Name = %s"""
                sql_value = (0, i[0] )
                mycursor.execute(sql_update, sql_value)
                mydb.commit()

    return render_template("index.html")


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        contact = request.form['contact']
        email = request.form['email']
        pass_word = request.form['pass_word']
        pass_c = request.form['pass_c']

        if pass_word == pass_c:
            mycursor = mydb.cursor()
            sql_insert = """INSERT INTO Users (First_Name, Last_Name, Phone_Number, Email, Password)
                            VALUES (%s, %s, %s, %s, %s)"""
            sql_value = (fname, lname, contact, email, pass_word)
            mycursor.execute(sql_insert, sql_value)
            mydb.commit()

            return redirect ("http://127.0.0.1:5000/")
        else:
            flash("Password fields do not match", "error")
        
    return render_template("sign_up.html")

@app.route("/user_reservation", methods=['GET', 'POST'])
def user_reservation():
    # msg = ''
    # # if request.method == 'POST':
    # email = session["email"]

    # mycursor = mydb.cursor()
    # mycursor.execute('Select First_Name from users where Email = %s', (email))
    # msg = mycursor.fetchone()
    if request.method == 'POST':
        session['name2'] = request.form['name2']
        session['contact'] = request.form['contact']
        session['email'] = request.form['email']
        session['datetime'] = request.form['datetime']
        session['count'] = request.form['count']

        return redirect ("/final_booking")

    return render_template("user_reservation.html")

@app.route("/reservation", methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        session['name2'] = request.form['name2']
        session['contact'] = request.form['contact']
        session['email'] = request.form['email']
        session['datetime'] = request.form['datetime']
        session['count'] = request.form['count']

        return redirect ("/final_booking")

    return render_template("reservation.html")
 

@app.route("/final_booking", methods=['GET', 'POST'])
def final_booking():
    mycursor = mydb.cursor()

    mycursor.execute('SELECT Table_Name FROM Bookings WHERE Capacity = %s AND Booked = %s', (session["count"], 0,)) 
    
    result = mycursor.fetchall()
    # print(result)
    # print(session["datetime"][11:])

    if request.method == 'POST':
        # print(request.form["option"])        

        sql_update = """UPDATE Bookings 
                        SET Name = %s, Phone = %s, Email = %s, Date = %s, Time = %s, Booked = %s
                        WHERE Table_Name = %s"""
        sql_value = (session["name"], session["contact"], session["email"], session["datetime"][:10], session["datetime"][11:], 1, request.form["option"] )
        mycursor.execute(sql_update, sql_value)
        mydb.commit()

        return redirect ("/success")
        
    return render_template("final_booking.html", result = result)


@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    

    app.run(debug = True)