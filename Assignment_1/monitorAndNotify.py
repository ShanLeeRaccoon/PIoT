from sense_hat import SenseHat
from datetime import datetime
from time import sleep
import sqlite3
from sqlite3 import Error
import os
import json



def get_cpu_temp():
    """
    Getting cpu temp for accurate temperature
    """
    res = os.popen("vcgencmd measure_temp").readline()
    return float(res.replace("temp=","").replace("'C\n",""))

def get_smooth(x):
    """
    Use moving average to smooth readings
    """
    if not hasattr(get_smooth, "t"):
        get_smooth.t = [x,x,x]
    
    get_smooth.t[2] = get_smooth.t[1]
    get_smooth.t[1] = get_smooth.t[0]
    get_smooth.t[0] = x

    return (get_smooth.t[0] + get_smooth.t[1] + get_smooth.t[2]) / 3


def create_connection(db_file):
    """
    creating connection with database with props 
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return(conn)


def create_table(conn, create_table_sql):
    """
    creating table in database
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def get_lowest_temp(cur):
    """
    getting the lowest temperature from today's sensor report
    """
    time = datetime.now()
    timeDate = time.strftime("%x")
    cur.execute("SELECT temperature FROM sensorReport WHERE time LIKE ?",('%'+timeDate+'%',))
    report_temp = cur.fetchall()
    lowest_temp = min(report_temp)[0]
    
    return(lowest_temp)

def get_highest_temp(cur):
    """
    getting the highest temperature from today's sensor report
    """
    time = datetime.now()
    timeDate = time.strftime("%x")    
    cur.execute("SELECT temperature FROM sensorReport WHERE time LIKE ?",('%'+timeDate+'%',))
    report_temp = cur.fetchall()
    highest_temp = max(report_temp)[0]
    
    return(highest_temp)

def create_sensorReport(conn, sensorReport):
    """
    create data in sensorReport table
    """
    sql = ''' INSERT INTO sensorReport(time,temperature,humidity)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, sensorReport)
    conn.commit()

    print("Sensor report has been added to database")

    return cur.lastrowid

def create_notification(conn, notification):
    """
    create data in notification table
    """
    print("created notification date")
    sql = ''' INSERT INTO notification(notification_date, message)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, notification)
    conn.commit()

    print("Notification has been added to database")

    return cur.lastrowid

def send_notification(message):
    """
    sending notification to users via pushbullet, when there are no message sent before
    """
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
        print("Today already sent")

    print("Notification sent")

def get_current_time():
    """
    get the current time value
    """
    time = datetime.now()

    return time

def send_daily_notification():
    """
    This function will be called at 11:59PM, if no message has been sent throughout the day, a pushbullet notification will be sent.
    """
    database = r"/home/pi/Desktop/Assignment_1/sensordata.db"
    time = datetime.date(datetime.now())
    conn = create_connection(database)
    cur = conn.cursor()
    highest_temp = get_highest_temp(cur)
    lowest_temp = get_lowest_temp(cur)
    message = "Todays highest is " + str(highest_temp) + " degrees and the lowest is " + str(lowest_temp) + " degrees"
    cur.execute("SELECT notification_date FROM notification WHERE notification_date = ?", (time,))
    data = cur.fetchone()
    if data is None:
        print(message)
        os.system('/home/pi/Desktop/Assignment_1/pushbullet.sh {}'.format(message))

        with conn:
            notification = (time, message)
            notification_id = create_notification(conn, notification)
    else:
        print("Today already sent")



def add_data(cold_max,  hot_min, comfortable_min, comfortable_max, humidity_max, humidity_min):
    """ 
    collecting data such as temperature, humidity and time from sensehat,
    checking if the data are out of range to create an appropriate notification for pushbullet, 
    triggering send notification
    """
    database = r"/home/pi/Desktop/Assignment_1/sensordata.db"
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    t_cpu = get_cpu_temp()
    h = sense.get_humidity()
    t = (t1 + t2) / 2
    t_corr = t - ((t_cpu - t) / 1.5)
    t_corr = get_smooth(t_corr)
    temp = (round(t_corr,2))
    humid = (round(h,2))

    conn = create_connection(database)
    with conn:
        time = datetime.now()
        print("Temperature: ", temp)
        print("Humidity: ", humid)
        message = ""
        if t_corr > hot_min:
            message = "The weather is over hot_min limit."
            send_notification(message)
        elif t_corr < cold_max:
            message = "The weather is below cold_max limit."
            send_notification(message)
        elif h > humidity_max:
            message = "The humidity is too high."
            send_notification(message)
        elif h < humidity_min:
            message = "The humidity is too low."
            send_notification(message)
        timeDate = time.strftime("%x")
        timeTime = time.strftime("%X")
        time = timeDate + " " + timeTime
        sensorReport = (time, temp,
                    humid)
        sensorReport_id = create_sensorReport(conn, sensorReport)
    



def check_and_create_table():
    """
    Start the program by checking if the following tables exist, 
    if not create a new table, else it will proceed the python program
    """
    # sense.show_message("Gathering Data")
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
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_sensorReport_table)
        create_table(conn, sql_create_notification_table)
    else:
        print("Error! cannot create connection with database")

#define a checkpoint for the end of the day for sending notification
checkpoint = "2329"
sense = SenseHat()
#opening a json config file to read containing temperature, humidity limits/ range 
with open("/home/pi/Desktop/Assignment_1/config.json", "r") as read_file:
    print("Reading config.json")
    limit = json.load(read_file)

#run table checking a program startup
check_and_create_table()
x = True
y = 4
#start main program with a 60 second interval adding new sensor data, and trigger send daily notification function when the current time is 11:59PM
while True:
    
    if x:
        for i in range(y):
            t1 = sense.get_temperature_from_humidity()
            t2 = sense.get_temperature_from_pressure()
            t_cpu = get_cpu_temp()
            h = sense.get_humidity()
            t = (t1 + t2) / 2
            t_corr = t - ((t_cpu - t) / 1.5)
            t_corr = get_smooth(t_corr)
            
        x = False
    
        
        
        
    add_data(limit["cold_max"],  limit["hot_min"], limit["comfortable_min"], limit["comfortable_max"], limit["humidity_max"], limit["humidity_min"])
    sleep(60)
    tempTime = datetime.now()
    time = tempTime.strftime("%H") + tempTime.strftime("%M")
    print("The current time is " + time)
    if checkpoint == time:
         send_daily_notification()

   
  
    

