# Importing all the libraries
from flask import Flask, render_template, url_for, request, flash, redirect, session
import pymysql
from flask_session import Session
from flask_mail import Mail, Message
import datetime

application = Flask(__name__)

# Configuration of Database Part
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="Restaurant_Reservation"    
)


# Configuration of sessions to store cache data
application.config["SESSION_PERMANENT"] =  False
application.config["SESSION_TYPE"] = "filesystem"
Session(application)
application.secret_key = ""


# Configuration of SMTP for sending emails
application.config['MAIL_SERVER']='smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USERNAME'] = ''
application.config['MAIL_PASSWORD'] = ''
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True
mail = Mail(application)


#----------------------------------------------Routing Part Starts From Here--------------------------------------#

# Home Page routing/function for the Application, where it ask a registered user to login or else click on guest user
@application.route("/", methods=['GET', 'POST'])
def home_page():
    if request.method == "POST":
        email_login = request.form['email_login']
        pass_login = request.form['pass_login']  
              
        mycursor = conn.cursor()
        mycursor.execute('SELECT * FROM Users WHERE Email = %s AND Password = %s', (email_login, pass_login, ))
        account = mycursor.fetchone()    
        if account:            
            session['name'] = "Hello " + account[0]
            return redirect ("/user_reservation")
        else:
           flash("Email and/or password is incorrect.", "error")

    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%m-%d")       
    now_time = now.strftime("%H:%M:%S")    
    user_date = now_date.replace('-','_')
    
    mycursor = conn.cursor()
    mycursor.execute("SHOW TABLES")
    tables_list = mycursor.fetchall()
    if tuple((user_date,)) in tables_list:
        mycursor.execute('SELECT * FROM %s WHERE Booked = %s'% (user_date,1,))
        bookings_ = mycursor.fetchall()          
        for i in bookings_:                        
            current = datetime.datetime.strptime(now_time,"%H:%M:%S").replace(year=datetime.datetime.today().year, month=datetime.datetime.today().month, day=datetime.datetime.today().day)
            entry = datetime.datetime.strptime(i[6],"%H:%M").replace(year=datetime.datetime.today().year, month=datetime.datetime.today().month, day=datetime.datetime.today().day)
            time_interval = current - entry          
            if time_interval > datetime.timedelta(hours= 1 , minutes=00, seconds=0):
                mycursor.execute("""UPDATE %s SET Name = NULL, Phone = NULL, Email = NULL, Date = NULL, Time = NULL, Booked = 0 WHERE Table_Name = '%s' """% (user_date, i[0],))
                conn.commit()            

    return render_template("index.html")


# SignUp Page form routing/function to register the user for this Application
@application.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        contact = request.form['contact']
        email = request.form['email']
        pass_word = request.form['pass_word']
        pass_c = request.form['pass_c']

        mycursor = conn.cursor()
        mycursor.execute("CREATE TABLE if not exists Users (First_Name VARCHAR(255), Last_Name VARCHAR(255), Phone_Number VARCHAR(255), Email VARCHAR(255) PRIMARY KEY, Password VARCHAR(255))")
        mycursor.execute('SELECT * FROM Users WHERE Email = %s',(email, ))
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
            sql_insert = """INSERT INTO Users (First_Name, Last_Name, Phone_Number, Email, Password)
                            VALUES (%s, %s, %s, %s, %s)"""
            sql_value = (fname, lname, contact, email, pass_word)
            mycursor.execute(sql_insert, sql_value)
            conn.commit()

            msg = Message('Registration Confirmation', sender = '', recipients = [email])
            msg.body =  "Hello " + fname + " " + lname + ",\n\n" + "Thanks for registering with Registro, one click app for Restaurant Table Reservation." + "\n\n" + "Regards,\n" + "Registro Team"
            mail.send(msg)

            return redirect ("/")
        
    return render_template("sign_up.html")

# Forgot Password Page form where user can update their password if they have forgottten
@application.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        mycursor = conn.cursor()
        mycursor.execute('SELECT * FROM Users WHERE Email = %s',(email, ))
        account = mycursor.fetchone()

        if not account:
            flash("Email does not exists")

        elif new_password != confirm_password:
            flash("Password fields do not match", "error")

        elif len(new_password) < 7:
            flash("Password must contain at least 7 characters.")

        else:
            mycursor.execute ('UPDATE Users SET Password = %s where Email = %s',(new_password, email,) )
            conn.commit()
            return redirect ("/")

    return render_template("forgot_password.html")


# Reservation Page form routing/function for a logged in user where they enter all the details for the Table reservation
@application.route("/user_reservation", methods=['GET', 'POST'])
def user_reservation():
    if request.method == 'POST':
        session['name2'] = request.form['name2']
        session['contact'] = request.form['contact']
        session['email'] = request.form['email']
        session['datetime'] = request.form['datetime']
        session['count'] = request.form['count']

        if len(request.form['contact']) != 10:
            flash("Invalid Phone No.")
            return redirect("/user_reservation")

        mycursor = conn.cursor()
        mycursor.execute('SHOW TABLES')     
        tables = mycursor.fetchall()
        user_date = session["datetime"][:10].replace('-','_')
        bool_value = True
        
        for i in tables:
            if user_date in i:
                bool_value = False
                break

        if bool_value == True:
            mycursor.execute("""CREATE TABLE %s  (Table_Name VARCHAR(255), Capacity VARCHAR(255), Name VARCHAR(255), Phone VARCHAR(255), Email VARCHAR(255), Date VARCHAR(255), Time VARCHAR(255), Booked BOOL)"""% (user_date, ))

            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 1", "2")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 2", "2")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 3", "2")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 4", "2")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 5", "2")"""% (user_date,))

            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 6", "4")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 7", "4")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 8", "4")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 9", "4")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 10", "4")"""% (user_date,))
            
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 11", "6")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 12", "6")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 13", "6")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 14", "6")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 15", "6")"""% (user_date,))
            
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 16", "8")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 17", "8")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 18", "8")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 19", "8")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 20", "8")"""% (user_date,))

            mycursor.execute("""UPDATE %s SET Booked = 0"""% (user_date,))
            mycursor.execute("""ALTER TABLE %s ADD PRIMARY KEY (Table_Name)"""% (user_date))
            conn.commit()

        return redirect ("/final_booking")

    return render_template("user_reservation.html")  


# Reservation Page form routing/function for a guest user where they enter all the details for the Table reservation
@application.route("/guest_reservation", methods=['GET', 'POST'])
def guest_reservation():
    session['name'] = ""
    if request.method == 'POST':
        session['name2'] = request.form['name2']
        session['contact'] = request.form['contact']
        session['email'] = request.form['email']
        session['datetime'] = request.form['datetime']
        session['count'] = request.form['count']

        if len(request.form['contact']) != 10:
            flash("Invalid Phone No.")
            return redirect("/guest_reservation")

        mycursor = conn.cursor()
        mycursor.execute('SHOW TABLES')     
        tables = mycursor.fetchall()
        user_date = session["datetime"][:10].replace('-','_')
        bool_value = True
        
        for i in tables:
            if user_date in i:
                bool_value = False
                break

        if bool_value == True:
            mycursor.execute("""CREATE TABLE %s  (Table_Name VARCHAR(255), Capacity VARCHAR(255), Name VARCHAR(255), Phone VARCHAR(255), Email VARCHAR(255), Date VARCHAR(255), Time VARCHAR(255), Booked BOOL)"""% (user_date, ))

            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 1", "2")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 2", "2")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 3", "2")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 4", "2")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 5", "2")"""% (user_date,))

            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 6", "4")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 7", "4")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 8", "4")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 9", "4")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 10", "4")"""% (user_date,))
            
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 11", "6")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 12", "6")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 13", "6")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 14", "6")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 15", "6")"""% (user_date,))
            
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 16", "8")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 17", "8")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 18", "8")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 19", "8")"""% (user_date,))
            mycursor.execute ("""INSERT INTO %s (Table_Name, Capacity) VALUES ("Table 20", "8")"""% (user_date,))

            mycursor.execute("""UPDATE %s SET Booked = 0"""% (user_date,))
            mycursor.execute("""ALTER TABLE %s ADD PRIMARY KEY (Table_Name)"""% (user_date))
            conn.commit()

        return redirect ("/final_booking")

    return render_template("guest_reservation.html")


# Final booking Page routing/function where available Tables are displayed and user selects the Table and books it
@application.route("/final_booking", methods=['GET', 'POST'])
def final_booking():
    user_date = session["datetime"][:10].replace('-','_')
    mycursor = conn.cursor()
    mycursor.execute('SELECT Table_Name FROM %s WHERE Capacity = %s AND Booked = %s ORDER BY Table_Name'% (user_date, session["count"], 0,))     
    result = mycursor.fetchall()    

    mycursor.execute("""SELECT COUNT(Table_Name) FROM %s WHERE Booked = 1"""% (user_date,))
    result2 = mycursor.fetchone()

    if request.method == 'POST':      
        mycursor.execute("""UPDATE %s SET Name = '%s', Phone = '%s', Email = '%s', Date ='%s', Time = '%s', Booked = %s WHERE Table_Name = '%s' """% (user_date, session["name2"], session["contact"], session["email"], session["datetime"][0:10], session["datetime"][11:], 1, request.form["option"],))
        conn.commit()

        msg = Message('Booking Confirmation', sender = '', recipients = [session["email"]])
        msg.body =  "Congratulations " + session["name2"] + ", your Table is booked on " + session["datetime"][:10] + " at " + session["datetime"][11:] + " for " + session['count'] + " number of guests. Thanks for Booking with Registro."
        mail.send(msg)

        return redirect ("/success")
        
    return render_template("final_booking.html", result = result, result2 = result2)


# Success page routing/function where a message is displayed to user of their booking
@application.route("/success")
def success():
    return render_template("success.html")



if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    
    application.run(debug = True)