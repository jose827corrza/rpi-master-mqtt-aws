from mqtt_connection import mqtt_connect, mqtt_disconnect
from mqtt_basic import pub_to_mqtt_topic

from station import  get_temp_pressure, get_lux

from json import dumps
from time import sleep
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

scheduler = BlockingScheduler()

def convert_to_station_json():
    lux = get_lux()
    temp, press = get_temp_pressure()
    print(f"Temp {temp}	Press: {press}	Lux: {lux}")
    message = dict()
    message['device'] = 'rpi-master'
    message['mode'] = 'STATION'
    message['signal'] = None
    message['data'] = {
        'temperature': {
            'value': temp,
            'magnitude': '°C'
            },
        'pressure': {
            'value': press,
            'magnitude': 'Pa'
            },
        'luminity': {
            'value': lux,
            'magnitude': 'Lumen'
            }
        }
#     message['currentNumber'] = number
    json_message = dumps(message)
    return json_message
    
def task():
    now = datetime.now()
    str_now = now.strftime("%H:%M:%S")
    print(f"Desde aca va una hora: {str_now}")
    mqtt_connect()
    payload = convert_to_station_json()
    pub_to_mqtt_topic(payload)
    sleep(1)
    mqtt_disconnect()
print("antes del add job")
scheduler.add_job(task, 'interval', hours = 1)
scheduler.start()
# mqtt_connect()
# number = 0
# while number < 10:
#     payload = convert_to_station_json(number)
#     pub_to_mqtt_topic(payload)
#     number+=1
#     sleep(1)
    
# mqtt_disconnect()