import flask
from flask import request, jsonify
import sqlite3
from datetime import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True




def dict_factory(cursor, row):
    """ 
    Sort data as dictionaries
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_last_id():
    """
    Getting the last id from sensorReport table
    """
    DATABASE = r"/home/pi/Desktop/Assignment_1/sensordata.db"
    
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        last_id = cur.execute('SELECT sensorReport_id FROM sensorReport ORDER BY sensorReport_id DESC LIMIT 1;').fetchone()
        return last_id

#API Get method (Default Route)
@app.route('/', methods=['GET'])
def home_route():
    return '''<h1>FuShan incorporated</h1>
<p>A default Route.</p>'''

#API Get Method (fetch the lastest data)
@app.route('/sensorData', methods=['GET'])
def api_all():
    """
    Connect to database and collect newest sensorReport data in dictionary form
    """
    conn = sqlite3.connect('/home/pi/Desktop/Assignment_1/sensordata.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    newest_sensorReports = cur.execute('SELECT * FROM sensorReport ORDER BY sensorReport_id DESC LIMIT 1;').fetchone()

    return jsonify(newest_sensorReports)


#Handle API Error
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>FuShan Incorporated: Wrong direct.</p>", 404


def insert_sensorData(sensorReport):
    """
    Add data to database
    """
    DATABASE = r"/home/pi/Desktop/Assignment_1/sensordata.db"
    
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        sql = ''' INSERT INTO sensorReport(time,temperature,humidity)
              VALUES(?,?,?) '''
        cur.execute(sql, sensorReport)
        con.commit()
        return cur.lastrowid




#API POST method 
@app.route("/sensorData", methods=['POST'])
def post_sensorData():
    """
    Request json format temperature and humidity from user and call insert function
    """
    if request.method == 'POST':
        temperature = request.json['temperature']     
        humidity = request.json['humidity']
        time = datetime.now()
        timeDate = time.strftime("%x")
        timeTime = time.strftime("%X")
        time = timeDate + " " + timeTime
        sensorReport = (time, temperature,
                    humidity)

        sensorReport_id = insert_sensorData(sensorReport)

        returned_value = api_all()
        
        return returned_value
    else:
        print("post fail")

def update_sensorReport(temperature, humidity):
    """
    Update temperature and humidity in database
    """
    DATABASE = r"/home/pi/Desktop/Assignment_1/sensordata.db"
    
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        latest_ID = int(get_last_id()[0])
        
        sql = ''' UPDATE sensorReport
              SET temperature = ? ,
                  humidity = ? 
                  WHERE sensorReport_id = ?'''
      
        cur.execute(sql, (temperature, humidity, latest_ID))
        con.commit()
        
#API PUT method
@app.route("/sensorData", methods=["PUT"])
def sensorData_update():
    """
    Request json format temperature and humidity from user and call update function
    """
    if request.method == 'PUT':
        temperature = request.json['temperature']     
        humidity = request.json['humidity']

        update_sensorReport(temperature, humidity)

        returned_value = api_all()
        
        return returned_value
    else:
        print("update fail")

#start server
app.run()