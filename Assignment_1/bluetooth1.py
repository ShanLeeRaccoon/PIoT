import os
import bluetooth
import json
import sqlite3
from sqlite3 import Error
from sense_hat import SenseHat

target_phone = "Galaxy S20 Ultra LTE"
target_mac_address = None

nearby_devices = bluetooth.discover_devices()
sense = SenseHat()

with open("config_min_max.json", "r") as read_file:
    print("test read")
    limit = json.load(read_file)

def send_bt_message():
    for add in nearby_devices:           
        os.system("hcitool scan")
        # print(bluetooth.lookup_name(add))
        if target_phone == bluetooth.lookup_name(add):
            target_mac_address = add
            print("Searching for target device: " + target_mac_address)
            os.system("obexftp --nopath --uuid none --bluetooth %s --channel 12 -p /home/pi/Desktop/Assignment_1/WeatherStatus.txt" % target_mac_address)
            break

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

def get_temperature():
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    t_cpu = get_cpu_temp()
    # p = sense.get_pressure()
    t = (t1 + t2) / 2
    t_corr = t - ((t_cpu - t) / 1.5)
    t_corr = get_smooth(t_corr)

    return t_corr

def get_humidity():
    h = sense.get_humidity()

    return h

def write_report(temp, humid):
    f = open("WeatherStatus.txt", "w")

    if temp < limit["min_temperature"]:
        f.write("The current temperature is " + str(limit["min_temperature"] - temp) + " Degree below the minimum temperature. \n")
        if humid < limit["min_humidity"]:
            f.write("The current humidity is " + str(limit["min_humidity"] - humid) + " Percent below the minimum humidity.")
        elif humid > limit["max_humidity"]:
            f.write("The current humidity is " + str(humid - limit["max_humidity"] ) + " Percent above the maximum humidity.")
        else:
            f.write("The current humidity is " + str(humid) + " Percent, and is within the comfortable range.")

    elif temp > limit["max_temperature"]:
        f.write("The current temperature is " + str(temp - limit["max_temperature"]) + " Degree above the maximum temperature. \n")
        if humid < limit["min_humidity"]:
            f.write("The current humidity is " + str(limit["min_humidity"] - humid) + " Percent below the minimum humidity.")
        elif humid > limit["max_humidity"]:
            f.write("The current humidity is " + str(humid - limit["max_humidity"] ) + " Percent above the maximum humidity.")
        else:
            f.write("The current humidity is " + str(humid) + " Percent, and is within the comfortable range.")
    else:
        f.write("The current temperature is " + str(temp)+ " Degree, and it is within the comfortable range. \n" )
        if humid < limit["min_humidity"]:
            f.write("The current humidity is " + str(limit["min_humidity"] - humid) + " Percent below the minimum humidity.")
        elif humid > limit["max_humidity"]:
            f.write("The current humidity is " + str(humid - limit["max_humidity"] ) + " Percent above the maximum humidity.")
        else:
            f.write("The current humidity is " + str(humid) + " Percent, and is within the comfortable range.")


    f.close()
    
    

temperature = get_temperature()
humidity = get_humidity()


if __name__ == '__main__':
    print(get_temperature())
    write_report(temperature, humidity)
    send_bt_message()
#     # print ("hciconfig hci0 piscan")
#     # os.system("sudo hciconfig hci0 piscan")
#     # print ("hciconfig hci0 name 'raspberrypi'")
#     # os.system("sudo hciconfig hci0 name 'raspberrypi'")
#     # print ("Scan Blt")
#     # os.system("sudo python /usr/share/doc/python-bluez/examples/simple/inquiry.py")

#     # with open("bluetooth_ID.txt", "r") as file :
#     #     id_blt = file.read()
#     #     file.close()

#     # print (id_blt)

#     # https://tutorials-raspberrypi.com/raspberry-pi-bluetooth-data-transfer-to-the-smartphone/

#     print ("Send File apk client")
#     os.system("obexftp --nopath --uuid none --bluetooth FC:DE:90:C2:9C:2A --channel 12 -p ~/dume.txt")