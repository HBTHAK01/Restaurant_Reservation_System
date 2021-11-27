from datetime import datetime
# from dns.rdatatype import NULL
from flask import Flask, render_template, url_for, request, flash, redirect, session
from flask_session import Session
import mysql.connector
from werkzeug.utils import redirect
import datetime


app = Flask(__name__)


#add
app.config["SESSION_PERMANENT"] =  False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.secret_key = "abc"  

# Database Part for MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Restaurant_Reservation"
)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        email_login = request.form['email_login']
        pass_login = request.form['pass_login']  
        mycursor = mydb.cursor()

        mycursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email_login, pass_login, ))
        account = mycursor.fetchone()
        # print(account)

        if account:
            session['name'] = account[0] 

            return redirect ("/user_reservation")
        else:
           flash("Email and/or password is incorrect.", "error")

    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM bookings WHERE Booked = %s', (1,))
    bookings_ = mycursor.fetchall()

    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")
    now_time = now.strftime("%H:%M:%S")

    for i in bookings_:
        if now_date == i[5]:
            current = datetime.datetime.strptime(now_time,"%H:%M:%S")
            entry = datetime.datetime.strptime(i[6],"%H:%M")
            time_interval = current - entry
            if time_interval > datetime.timedelta(hours= 1 , minutes=00, seconds=0):
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

        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM users WHERE email = %s',(email, ))
        account = mycursor.fetchone()

        if account:
            flash("Email already exists")

        elif len(contact) != 10:
            flash("Invalid Phone No.")

        elif pass_word != pass_c:
            flash("Password fields do not match", "error")

        elif len(pass_word) < 7:
            flash("Password must contain at least 7 characters.")

        else:
            # mycursor = mydb.cursor()
            sql_insert = """INSERT INTO Users (First_Name, Last_Name, Phone_Number, Email, Password)
                            VALUES (%s, %s, %s, %s, %s)"""
            sql_value = (fname, lname, contact, email, pass_word)
            mycursor.execute(sql_insert, sql_value)
            mydb.commit()

            return redirect ("http://127.0.0.1:5000/")
        
    return render_template("sign_up.html")

@app.route("/user_reservation", methods=['GET', 'POST'])
def user_reservation():            
    if request.method == 'POST':
        session['name2'] = request.form['name2']
        session['contact'] = request.form['contact']
        session['email'] = request.form['email']
        session['datetime'] = request.form['datetime']
        session['count'] = request.form['count']

        #Unit TEST needed
        if request.form['datetime'] :
            d1 = datetime.datetime.strptime(request.form['datetime'],"%Y-%m-%dT%H:%M")
            if d1 < datetime.datetime.now():
                flash("Invalid Date")  
                return redirect("/user_reservation")  
        return redirect ("/final_booking")

    return render_template("user_reservation.html")

@app.route("/guest_reservation", methods=['GET', 'POST'])
def guest_reservation():
    if request.method == 'POST':
        session['name2'] = request.form['name2']
        session['contact'] = request.form['contact']
        session['email'] = request.form['email']
        session['datetime'] = request.form['datetime']
        session['count'] = request.form['count']

        #Unit TEST needed
        if request.form['datetime'] :
            d1 = datetime.datetime.strptime(request.form['datetime'],"%Y-%m-%dT%H:%M")
            if d1 < datetime.datetime.now():
                flash("Invalid Date")  
                return redirect("/guest_reservation")  

        return redirect ("/final_booking")

    return render_template("guest_reservation.html")
 

@app.route("/final_booking", methods=['GET', 'POST'])
def final_booking():
    mycursor = mydb.cursor()

    mycursor.execute('SELECT Table_Name FROM Bookings WHERE Capacity = %s AND Booked = %s', (session["count"], 0,)) 
    
    result = mycursor.fetchall()
    if request.method == 'POST':

        sql_update = """UPDATE Bookings 
                        SET Name = %s, Phone = %s, Email = %s, Date = %s, Time = %s, Booked = %s
                        WHERE Table_Name = %s"""
        sql_value = (session["name2"], session["contact"], session["email"], session["datetime"][:10], session["datetime"][11:], 1, request.form["option"] )
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