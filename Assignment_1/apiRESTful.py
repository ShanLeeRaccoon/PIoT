import flask
from flask import request, jsonify
import sqlite3
from datetime import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True




def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_last_id():
    DATABASE = r"/home/pi/Desktop/Assignment_1/sensordata.db"
    
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        last_id = cur.execute('SELECT sensorReport_id FROM sensorReport ORDER BY sensorReport_id DESC LIMIT 1;').fetchone()
        return last_id
        
@app.route('/', methods=['GET'])
def home_route():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/sensorData', methods=['GET'])
def api_all():
    conn = sqlite3.connect('sensordata.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_sensorReports = cur.execute('SELECT * FROM sensorReport ORDER BY sensorReport_id DESC LIMIT 1;').fetchone()

    return jsonify(all_sensorReports)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

def insert_sensorData(sensorReport):
    DATABASE = r"/home/pi/Desktop/Assignment_1/sensordata.db"
    
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        sql = ''' INSERT INTO sensorReport(time,temperature,humidity)
              VALUES(?,?,?) '''
        cur.execute(sql, sensorReport)
        con.commit()
        return cur.lastrowid





@app.route("/sensorData", methods=['POST'])
def post_sensorData():
    if request.method == 'POST':
        temperature = request.json['temperature']     
        humidity = request.json['humidity']
        time = datetime.now()
        # time = request.json['time']
        
        sensorReport = (time.strftime("%c"), temperature,
                    humidity)

        sensorReport_id = insert_sensorData(sensorReport)

        returned_value = api_all()
        
        return returned_value
    else:
        print("ripho_post fail")

def update_sensorReport(temperature, humidity):
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
        

@app.route("/sensorData", methods=["PUT"])
def sensorData_update():
    if request.method == 'PUT':
        temperature = request.json['temperature']     
        humidity = request.json['humidity']
        
        # time = request.json['time']
        
        # sensorReport = (temperature, humidity)

        update_sensorReport(temperature, humidity)

        returned_value = api_all()
        
        return returned_value
    else:
        print("ripho_update fail")


# @app.route("/sensorData", methods=["POST"])
# def add_SensorData():
#     time = request.json['time']
#     temperature = request.json['temperature']
#     humidity = request.json['humidity']

#     new_sensorData = SensorData(time, temperature, humidity)

#     db.session.add(new_SensorData)
#     db.session.commit()

#     sensorData = SensorData.query.get(new_sensorData.id)

#     return sensorData_schema.jsonify(sensorData)


# @app.route('/api/v1/resources/books', methods=['GET'])
# def api_filter():
#     query_parameters = request.args

#     id = query_parameters.get('id')
#     published = query_parameters.get('published')
#     author = query_parameters.get('author')

#     query = "SELECT * FROM books WHERE"
#     to_filter = []

#     if id:
#         query += ' id=? AND'
#         to_filter.append(id)
#     if published:
#         query += ' published=? AND'
#         to_filter.append(published)
#     if author:
#         query += ' author=? AND'
#         to_filter.append(author)
#     if not (id or published or author):
#         return page_not_found(404)

#     query = query[:-4] + ';'

#     conn = sqlite3.connect('books.db')
#     conn.row_factory = dict_factory
#     cur = conn.cursor()

#     results = cur.execute(query, to_filter).fetchall()

#     return jsonify(results)

app.run()