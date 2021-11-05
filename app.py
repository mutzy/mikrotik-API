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
import pymysql.cursors
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.env = "Development"
app.debug = "True"
app.config['SECRET_KEY'] = '0af158fc013329a0492cc929d3fbee02'
#session handlers
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='mikrotik_api',
                             cursorclass=pymysql.cursors.DictCursor)

# creating the date object of today's date
todays_date = date.today()

# with connection:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#         cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()
@app.route('/')
def index():
    if session.get('username'):
        msg = 'connected'
        return render_template('index.html',username = session["username"],msg=msg)
    return redirect(url_for('login'))

@app.route("/login",methods=['POST','GET'])
def login():
    date = todays_date.year
    if request.method == 'POST' and len(request.form['username']) > 0:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `username`=%s AND `password`=%s"
            cursor.execute(sql, (request.form['username'], request.form['password']))
            result = cursor.fetchone()
            if result == None: 
                return render_template('login.html',date=date)
            else:
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