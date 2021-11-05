#!/usr/bin/python3
# -*- coding: latin-1 -*-
import sys, posix, time, binascii, socket, select, ssl
import hashlib
from flask import Flask, render_template, redirect, url_for, request, session
from flask_session import Session
from datetime import date
import ssl
from librouteros import connect
import paramiko
import pymysql
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.env = "Development"
app.debug = "True"
app.config['SECRET_KEY'] = '0af158fc013329a0492cc929d3fbee02'
#session handlers
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
#database
userpass = 'mysql+pymysql://root:@'
basedir  = '127.0.0.1'
dbname   = '/mikrotik_api'
socket   = '?unix_socket=/opt/lampp/var/mysql/mysql.sock'
dbname   = dbname + socket
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + basedir + dbname

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# creating the date object of today's date
todays_date = date.today()


@app.route('/')
def index():
    msg = ''
    if session.get('username'):
        if db.session.query('1').from_statement('SELECT 1').all():
            msg = 'It works.'
        else:
            msg =  'Something is broken.'
        return render_template('index.html',username = session["username"],msg=msg)
    return redirect(url_for('login'))

@app.route("/login",methods=['POST','GET'])
def login():
    date = todays_date.year
    if request.method == 'POST' and len(request.form['username']) > 0:
        # user = User.query.get(form.email.data)
        # if user:
        #     if bcrypt.check_password_hash(user.password, form.password.data):
        #         user.authenticated = True
        #         db.session.add(user)
        #         db.session.commit()
        #         login_user(user, remember=True)
        session['username'] = request.form['username']
        #api = connect(username='admin', password='', host='127.0.0.1')
        #ip_info = api(cmd="/ip/address/print")

        #for item in ip_info:
            #print(item)
        return redirect(url_for('index'))
    else:
        return render_template('login.html',date=date)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/dashboard")
def dashboard():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('192.168.0.110', username='admin', password='')
    stdin, stdout, stderr = client.exec_command('ip address print')

    for line in stdout:
        print(line.strip('\n'))
    client.close()


if __name__ == '__main__':
   app.run()