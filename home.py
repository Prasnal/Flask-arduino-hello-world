from flask import Flask, render_template, send_from_directory, session
from pyfirmata import *
app = Flask(__name__)

app.secret_key = b'\xae\n\x1cS\xc3\x8f>\xba\x80\x054\xd19\xff9\xc7'
a=Arduino('/dev/ttyACM0')
a.digital[4].mode=INPUT
it=util.Iterator(a)
it.start()

def check_status(status):
    if status:
        msg='wylaczona'
    else:
        msg='wlaczona'
    return msg

@app.route("/")
def hello():
    #send_from_directory('html','/home/krasnal/mgr_praca/mgr_project/home.html')
    #session['Arduino'] = a

    return render_template('home.html')


@app.route("/blue/", methods=['POST'])
def set_blue():
    status=a.digital[7].read()
    msg=check_status(status)
    a.digital[7].write(not status)
    print(a.digital[7].read())
    return render_template('home.html',stat_blue=msg)

@app.route("/green/", methods=['POST'])
def set_green():
    status=a.digital[8].read()
    msg=check_status(status)
    a.digital[8].write(not status)
    print(a.digital[8].read())
    return render_template('home.html',stat_green=msg)
