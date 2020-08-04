import os
import bluetooth
import json
import sqlite3
from sqlite3 import Error
from sense_hat import SenseHat



def send_bt_message():
    """
    Search for nearby bluetooth devices and search for targetted device to proceed sending WeatherStatus.txt file
    """
    for add in nearby_devices:           
        os.system("hcitool scan")
        if target_phone == bluetooth.lookup_name(add):
            target_mac_address = add
            print("Searching for target device: " + target_mac_address)
            os.system("obexftp --nopath --uuid none --bluetooth %s --channel 12 -p /home/pi/Desktop/Assignment_1/WeatherStatus.txt" % target_mac_address)
            break

def get_cpu_temp():
    """
    get cpu temperature for accurate room temperature
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

def get_temperature():
    """
    Get accurate temperature by using sensehat's temperature, smooth and cpu temperature to compute correct value
    """
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    t_cpu = get_cpu_temp()
    t = (t1 + t2) / 2
    t_corr = t - ((t_cpu - t) / 1.5)
    t_corr = get_smooth(t_corr)
    t_corr2 = (round(t_corr,0))

    return t_corr2

def get_humidity():
    """
    Get humidity value from sensehat
    """
    h = sense.get_humidity()
    h2 = (round(h,0))
    
    return h2

def write_report(temp, humid):
    """
    Generate WeatherStatus.txt for transfer via Bluetooth
    """
    print(humid)
    print(temperature)
    f = open("/home/pi/Desktop/Assignment_1/WeatherStatus.txt", "w")


    if temp < limit["min_temperature"]:
        f.write("The current temperature is " + str(temp) + " , " + str(limit["min_temperature"] - temp) + " Degree below the minimum temperature. \n")
        if humid < limit["min_humidity"]:
            f.write("The current humidity is " + str(humid) + " , " + str(limit["min_humidity"] - humid) + " Percent below the minimum humidity.")
        elif humid > limit["max_humidity"]:
            f.write("The current humidity is " + str(humid) + " , "+ str(humid - limit["max_humidity"] ) + " Percent above the maximum humidity.")
        else:
            f.write("The current humidity is " + str(humid) + " Percent, and is within the comfortable range.")

    elif temp > limit["max_temperature"]:
        f.write("The current temperature is " + str(temp) + " , " + str(temp - limit["max_temperature"]) + " Degree above the maximum temperature. \n")
        if humid < limit["min_humidity"]:
            f.write("The current humidity is " + str(humid) + " , " + str(limit["min_humidity"] - humid) + " Percent below the minimum humidity.")
        elif humid > limit["max_humidity"]:
            f.write("The current humidity is " + str(humid) + " , " + str(humid - limit["max_humidity"] ) + " Percent above the maximum humidity.")
        else:
            f.write("The current humidity is " + str(humid) + " Percent, and is within the comfortable range.")
    else:
        f.write("The current temperature is " + str(temp)+ " Degree, and it is within the comfortable range. \n" )
        if humid < limit["min_humidity"]:
            f.write("The current humidity is " + str(humid) + " , " + str(limit["min_humidity"] - humid) + " Percent below the minimum humidity.")
        elif humid > limit["max_humidity"]:
            f.write("The current humidity is " + str(humid) + " , " + str(humid - limit["max_humidity"] ) + " Percent above the maximum humidity.")
        else:
            f.write("The current humidity is " + str(humid) + " Percent, and is within the comfortable range.")

    f.close()
    
#defining a target device name
target_phone = "Galaxy S20 Ultra LTE"
target_mac_address = None

#Lisintg discovered Nearby Devices
nearby_devices = bluetooth.discover_devices()
sense = SenseHat()

#opening a json config file to read containing temperature, humidity limits/ range 
with open("/home/pi/Desktop/Assignment_1/config_min_max.json", "r") as read_file:
    print("Reading config.json")
    limit = json.load(read_file)

temperature = get_temperature()
humidity = get_humidity()

#Start main program
if __name__ == '__main__':
    write_report(temperature, humidity)
    send_bt_message()