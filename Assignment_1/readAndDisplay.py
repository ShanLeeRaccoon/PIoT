import sqlite3
from sqlite3 import Error
from sense_hat import SenseHat
from time import sleep
import json


def create_connection(db_file):
    """
    create connection with database with props 
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_last_record(conn):
    """
    Acqure last(Newest) record from sensorReport
    """
    cur = conn.cursor()
    cur.execute("SELECT temperature FROM sensorReport ORDER BY sensorReport_id DESC LIMIT 1")

    temp = cur.fetchone()
    display_temp(temp)


def display_temp(temp):
    """
    Display newest temperature(props) from sensorReport on senseHat with cordinating colors
    """
    a = temp[0]
    b = (round(a,1))
    c = str(b)
    print("Newest Recorded Temperature: " + c)
    if b < limit["cold_max"]:
        sense.show_message(c + " Degrees" , text_colour = [50, 50, 255])
    elif b > limit["hot_min"]:
        sense.show_message(c + " Degrees" , text_colour = [255, 50, 50])
    else:
        sense.show_message(c + " Degrees" , text_colour = [50, 255, 50])





def connect_to_database():
    """
    Establish initial connection to database and trigger select last record function
    """

    database = r"/home/pi/Desktop/Assignment_1/sensordata.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        select_last_record(conn)

sense = SenseHat()
#Read json config file for temperature limit/ range
with open("config.json", "r") as read_file:
    print("Reading config.json")
    limit = json.load(read_file)

#Start main program with a 60 seconds interval
while True:
    connect_to_database()
    sleep(60)

