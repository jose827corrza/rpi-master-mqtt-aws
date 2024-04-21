from awscrt import mqtt
import threading
from json import dumps

from mqtt_connection import mqtt_conn


received_all_event = threading.Event()
received_count = 0

TOPIC = 'topic_2'


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    load = payload.decode()
    print("Received message from topic '{}': {}".format(topic, payload.decode()))
    if load == '2':
        on_off()
    elif load == '3':
        message = dict()
        message['delivered'] = True
        json_message = dumps(message)
        pub_to_mqtt_topic(json_message)
        #received_all_event.set()
    
def on_off():
    received_all_event.set()

def sub_to_mqtt_topic():
    sub_future, packed_id = mqtt_conn.subscribe(
        topic= TOPIC,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received
        )
    sub_future.result()
    received_all_event.wait()

def pub_to_mqtt_topic(payload):
    pub_future, packed_id = mqtt_conn.publish(
        topic = TOPIC,
        qos= mqtt.QoS.AT_LEAST_ONCE,
        payload = payload
        )
    