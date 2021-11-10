from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route("/reservation")
def reservation():
    return render_template("reservation.html")
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug = True)