from flask import Flask, render_template, send_from_directory, session, request, flash
from pyfirmata import *
from sqlalchemy.orm import sessionmaker
from dbtable import *
engine = create_engine('sqlite:///users.db', echo=True)

app = Flask(__name__)

app.secret_key = b'\xae\n\x1cS\xc3\x8f>\xba\x80\x054\xd19\xff9\xc7'
a=Arduino('/dev/ttyACM1')
a.digital[4].mode=INPUT
it=util.Iterator(a)
it.start()



def check_status(status):
    if status:
        msg='turned off'
    else:
        msg='turned on'
    return msg

@app.route("/")
def hello():
    #send_from_directory('html','/home/krasnal/mgr_praca/mgr_project/home.html')
    #session['Arduino'] = a

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    username = str(request.form['username'])
    password = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()

    query = s.query(User).filter(User.username.in_([username]),
                                 User.password.in_([password]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return hello()

@app.route('/logout/', methods=['POST'])
def do_logout():
    session['logged_in'] = False
    return hello()

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
