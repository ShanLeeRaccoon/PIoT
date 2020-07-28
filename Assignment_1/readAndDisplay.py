import sqlite3
from sqlite3 import Error
from sense_hat import SenseHat
from time import sleep
import json

sense = SenseHat()

with open("config.json", "r") as read_file:
    print("test read")
    limit = json.load(read_file)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT temperature FROM sensorReport ORDER BY sensorReport_id DESC LIMIT 1")

    temp = cur.fetchone()
    display_temp(temp)
    # for x in temp:
    #     print(x)


def display_temp(temp):
    
    a = temp[0]
    b = (round(a,1))
    c = str(b)
    if b < limit["cold_max"]:
        sense.show_message(c + " Degrees" , text_colour = [50, 50, 255])
    elif b > limit["hot_min"]:
        sense.show_message(c + " Degrees" , text_colour = [255, 50, 50])
    else:
        sense.show_message(c + " Degrees" , text_colour = [50, 255, 50])





def main():
    database = r"/home/pi/Desktop/Assignment_1/sensordata.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        select_all_tasks(conn)


while True:
    main()
    sleep(60)

