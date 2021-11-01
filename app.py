from flask import Flask, render_template, redirect, url_for
from datetime import date

app = Flask(__name__)
app.env = "Development"
app.debug = "True"

# creating the date object of today's date
todays_date = date.today()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route("/login")
def login():
    date = todays_date.year
    return render_template('login.html',date=date)

if __name__ == '__main__':
   app.run()