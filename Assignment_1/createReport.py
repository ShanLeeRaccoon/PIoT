import csv
import sqlite3
from sqlite3 import Error
from glob import glob;
from os.path import expanduser
from csv import writer
from csv import reader



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
    # conn.row_factory = sqlite3.Row
    cur_time = conn.cursor()
    cur_temp = conn.cursor()
    cur_time.execute("SELECT time FROM sensorReport")
    cur_temp.execute("SELECT temperature FROM sensorReport")

    report_time = cur_time.fetchall()
    report_temp = cur_temp.fetchall()

    # for x in report:
    #     print(x)
    status = status_handler(report_temp)
    create_CSV(report_time, status)
    


   
def create_CSV(report_time, status):
    
    with open("report_init.csv", "w", newline='') as csv_file: 
        csv_writer = csv.writer(csv_file)
        
        csv_writer.writerow(["Date","Status"])
        csv_writer.writerows(report_time)


        # for x in report:
        #     print(report[0])
        # for x in report:
        #     csv_writer.writerow(report["time"])
        # csv_writer.writerow([report_time[0] for i in report_time]) # write headers
        
        # csv_writer.writerows(report_time)
        
       
        # csv_writer.writerows(report_time)
        print("creating")
   
    

    with open('report_init.csv', 'r') as read_obj, \
            open('report.csv', 'w', newline='') as write_obj:
        csv_reader = reader(read_obj)
        csv_writer = writer(write_obj)
        index = 0
        next(csv_reader, None)
        csv_writer.writerow(["Date","Status"])
        for row in csv_reader:
        # Append the default text in the row / list
            
            # print(index)
            row.append(status[index])
        # Add the updated row / list to the output file
            csv_writer.writerow(row)
            index = index + 1






def status_handler(temperature_list):
    status = []
    for x in temperature_list:
        a = x[0]
        b = (round(a,1))
        c = int(b)
        
        if c < 10:
            status.append("BAD:" + str(10-c) +" below the comfort temperature")
        elif c > 25:
            status.append("BAD:" + str(c-25) +" above the comfort temperature")
        else:
            status.append("OK")
    return status

            
        
        
    



def main():
    database = r"/home/pi/Desktop/Assignment_1/sensordata.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        select_all_tasks(conn)



if __name__ == '__main__':
    main()
    



