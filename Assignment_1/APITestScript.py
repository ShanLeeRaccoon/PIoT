import requests
import json

#apiRESTful.py is required to be executed in order to run the APITestScript

def get_newest_data():
    """
    Get newest sensorReport data function
    """
    url = "http://127.0.0.1:5000/sensorData"

    response = requests.request("GET", url)
    print(response.text)


def post_sensor_data(humidity, temperature):
    """
    A post script to add new sensorReport data
    """
    url = "http://127.0.0.1:5000/sensorData"

    data = {'humidity': humidity, 'temperature': temperature}
    payload = json.dumps(data)
    headers = {
        'content-type': "application/json",
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

def update_lastest_sensor_data(humidity, temperature):
    """
    An UPDATE script to update the lastest sensorReport data
    """
    url = "http://127.0.0.1:5000/sensorData"
    data = {'humidity': humidity, 'temperature': temperature}
    payload = json.dumps(data)
    headers = {
        'content-type': "application/json",
        }
    response = requests.request("PUT", url, data=payload, headers=headers)
    print(response.text)


get_newest_data()

#post_sensor_data(99,46)
#update_lastest_sensor_data(69,46)

