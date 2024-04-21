from mqtt_connection import mqtt_connect, mqtt_disconnect
from mqtt_basic import pub_to_mqtt_topic

from json import dumps
from time import sleep

def convert_to_station_json(number):
    message = dict()
    message['device'] = 'rpi-master'
    message['mode'] = 'STATION'
    message['signal'] = None
    message['data'] = {
        'test': number
        }
    message['currentNumber'] = number
    json_message = dumps(message)
    return json_message
    
mqtt_connect()
number = 0
while number < 10:
    payload = convert_to_station_json(number)
    pub_to_mqtt_topic(payload)
    number+=1
    sleep(1)
    
mqtt_disconnect()