# How to run project
1. pip install -r requirements.txt
2. Upload StandardFirmata to Arduino (via Arduino IDE)
3. `sudo chmod 666 /dev/ttyACM0`
4. `export FLASK_APP=home.py`
5. flask run
