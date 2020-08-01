import csv
import sqlite3
from sqlite3 import Error
from glob import glob
from os.path import expanduser
from csv import writer
from csv import reader
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

def select_time_temp(conn):
    """
    Select all time and temperature data from sensorReport table
    """
    cur_time = conn.cursor()
    cur_temp = conn.cursor()
    cur_time.execute("SELECT time FROM sensorReport")
    cur_temp.execute("SELECT temperature FROM sensorReport")

    report_time = cur_time.fetchall()
    report_temp = cur_temp.fetchall()

    status = status_handler(report_temp)
    create_CSV(report_time, status)
    


   
def create_CSV(report_time, status):
    """
    Create CSV file with headers and add report time and cordinating temperature status(prosp)
    """
    #initialize a csv file with time column
    with open("report_init.csv", "w", newline='') as csv_file: 
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Date","Status"])
        csv_writer.writerows(report_time)
        print("creating")
    #create main csv file according to the initial csv file
    with open('report_init.csv', 'r') as read_obj, \
            open('report.csv', 'w', newline='') as write_obj:
        csv_reader = reader(read_obj)
        csv_writer = writer(write_obj)
        index = 0
        next(csv_reader, None)
        csv_writer.writerow(["Date","Status"])
        for row in csv_reader:
            row.append(status[index])
            csv_writer.writerow(row)
            index = index + 1






def status_handler(temperature_list):
    """
    return a list of temperature status, compared with config json
    """
    status = []
    for x in temperature_list:
        a = x[0]
        b = (round(a,1))
        c = int(b)
        
        if c < limit["comfortable_min"]:
            status.append("BAD:" + str(limit["comfortable_min"]-c) +" below the comfort temperature")
        elif c > limit["comfortable_max"]:
            status.append("BAD:" + str(c-limit["comfortable_max"]) +" above the comfort temperature")
        else:
            status.append("OK")
    return status

            
        
        
    



def connect_to_database():
    """
    Establish initial connection to database and trigger select time and temperature function
    """
    database = r"/home/pi/Desktop/Assignment_1/sensordata.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        select_time_temp(conn)

#Read json config file for temperature limit/ range
with open("config.json", "r") as read_file:
    print("Reading config.json")
    limit = json.load(read_file)
#Start main program
if __name__ == '__main__':
    connect_to_database()
    



