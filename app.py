#!/usr/bin/python3
# -*- coding: latin-1 -*-
import sys, posix, time, binascii, socket, select, ssl
import hashlib
from flask import Flask, render_template, redirect, url_for
from datetime import date
import resources

app = Flask(__name__)
app.env = "Development"
app.debug = "True"
app.config['SECRET_KEY'] = '0af158fc013329a0492cc929d3fbee02'


# creating the date object of today's date
todays_date = date.today()

def open_socket(dst, port, secure=False):
  s = None
  res = socket.getaddrinfo(dst, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
  af, socktype, proto, canonname, sockaddr = res[0]
  skt = socket.socket(af, socktype, proto)
  if secure:
    s = ssl.wrap_socket(skt, ssl_version=ssl.PROTOCOL_TLSv1_2, ciphers="ADH-AES128-SHA256") #ADH-AES128-SHA256
  else:
    s = skt
  s.connect(sockaddr)
  return print(s)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route("/login")
def login():
    date = todays_date.year
    s = None
    dst = '127.0.0.1'
    user = "admin"
    passw = ""
    secure = False
    port = 0

    # use default username and pasword if not specified
    
    user = "admin"
    passw = ""
    print(str(dst)+""+str(port)+""+str(secure))
    if (port==0):
      port = 8080 if secure else 8728

    s = open_socket(dst, port, secure)
    
    if s is None:
      print ('could not open socket')
      sys.exit(1)

    apiros = resources.ApiRos(s)
    if not apiros.login(user, passw):
      return

    inputsentence = []

    while 1:
        r = select.select([s, sys.stdin], [], [], None)
        if s in r[0]:
            # something to read in socket, read sentence
            x = apiros.readSentence()

        if sys.stdin in r[0]:
            # read line from input and strip off newline
            l = sys.stdin.readline()
            l = l[:-1]

            # if empty line, send sentence and start with new
            # otherwise append to input sentence
            if l == '':
                apiros.writeSentence(inputsentence)
                inputsentence = []
            else:
                inputsentence.append(l)
    return render_template('login.html',date=date,inputsentence=inputsentence)

if __name__ == '__main__':
   app.run()