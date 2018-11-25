from flask import Flask, render_template, send_from_directory, session, request, flash
from pyfirmata import *

app = Flask(__name__)

app.secret_key = b'\xae\n\x1cS\xc3\x8f>\xba\x80\x054\xd19\xff9\xc7'
a = Arduino('/dev/ttyACM0')
it = util.Iterator(a)
it.start()

diode = {
    'kitchen': 7,
    'bathroom': 6,
    'hall': 5,
    'first_room': 4,
    'second_room': 3,
}

@app.route("/")
def hello():
    return render_template('home.html')

def check_status(status):
    if status:
        msg='turned off'
    else:
        msg='turned on'
    return msg

@app.route("/<room>/", methods=['POST'])
def set_diode(room):
    print(room)
    pin=diode[room]
    status=a.digital[pin].read()
    msg=check_status(status)
    a.digital[pin].write(not status)
    print(a.digital[pin].read())
    return render_template('home.html',stat=msg)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
