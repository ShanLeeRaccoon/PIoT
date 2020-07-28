from sense_hat import SenseHat
from datetime import datetime
from time import sleep
import sqlite3
from sqlite3 import Error
import os
import json

sense = SenseHat()

with open("config.json", "r") as read_file:
    print("test read")
    limit = json.load(read_file)
    
    print(limit["cold_max"])


def get_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    return float(res.replace("temp=","").replace("'C\n",""))

def get_smooth(x):
    if not hasattr(get_smooth, "t"):
        get_smooth.t = [x,x,x]
    
    get_smooth.t[2] = get_smooth.t[1]
    get_smooth.t[1] = get_smooth.t[0]
    get_smooth.t[0] = x

    return (get_smooth.t[0] + get_smooth.t[1] + get_smooth.t[2]) / 3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)

        return conn
    except Error as e:
        print(e)

    return(conn)


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_sensorReport(conn, sensorReport):
    sql = ''' INSERT INTO sensorReport(time,temperature,humidity)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, sensorReport)
    conn.commit()
    return cur.lastrowid

def create_notification(conn, notification):
    print("created notification date")
    sql = ''' INSERT INTO notification(notification_date, message)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, notification)
    conn.commit()
    return cur.lastrowid

def send_notification(message):
    database = r"/home/pi/Desktop/Assignment_1/sensordata.db"
    time = datetime.date(datetime.now())
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT notification_date FROM notification WHERE notification_date = ?", (time,))
    data = cur.fetchone()
    if data is None:
        print(message)
        os.system('/home/pi/Desktop/Assignment_1/pushbullet.sh {}'.format(message))

        with conn:
            notification = (time, message)
            notification_id = create_notification(conn, notification)
        
    else:
        print(".")
    

    
    print("sent")

def main():

    database = r"/home/pi/Desktop/Assignment_1/sensordata.db"

    sql_create_sensorReport_table = """ CREATE TABLE IF NOT EXISTS sensorReport (
                                        sensorReport_id integer PRIMARY KEY,
                                        time text NOT NULL,
                                        temperature float,
                                        humidity float
                                    ); """
    sql_create_notification_table = """ CREATE TABLE IF NOT EXISTS notification (
                                        notification_id integer PRIMARY KEY,
                                        notification_date text NOT NULL,
                                        message text
                                    ); """

    sense.show_message("Getting Sensor Data")

    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_sensorReport_table)
        create_table(conn, sql_create_notification_table)
    else:
        print("Error! cannot create the database connection.")


def add_data(cold_max,  hot_min, comfortable_min, comfortable_max, humidity_max, humidity_min):
    database = r"/home/pi/Desktop/Assignment_1/sensordata.db"
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    t_cpu = get_cpu_temp()
    h = sense.get_humidity()
    # p = sense.get_pressure()
    t = (t1 + t2) / 2
    t_corr = t - ((t_cpu - t) / 1.5)
    t_corr = get_smooth(t_corr)

    conn = create_connection(database)
    with conn:
        print("added")
        time = datetime.now()
        print(t_corr)
        message = ""
        #25
        if t_corr > hot_min:
            message = "The weather is over hot_min limit."
            send_notification(message)
        #10
        elif t_corr < cold_max:
            message = "The weather is below cold_max limit."
            send_notification(message)
        elif h > humidity_max:
            message = "The humidity is too high."
            send_notification(message)
        elif h < humidity_min:
            message = "The humidity is too low."
            send_notification(message)

        sensorReport = (time.strftime("%c"), t_corr,
                    h)
        sensorReport_id = create_sensorReport(conn, sensorReport)
    

def get_current_time():
    time = datetime.now()

    return time



if __name__ == '__main__':
    main()
    

while True:
    # print(get_current_time())
    add_data(limit["cold_max"],  limit["hot_min"], limit["comfortable_min"], limit["comfortable_max"], limit["humidity_max"], limit["humidity_min"])
    sleep(5)
