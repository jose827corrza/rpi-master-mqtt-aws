from awsiot import mqtt_connection_builder
from awscrt import mqtt

import threading
import json


received_all_event = threading.Event()
received_count = 0

MQTT_BROKER = 'a1gtemfhsymp11-ats.iot.us-east-1.amazonaws.com'
MQTT_PORT = 8883
MQTT_CERT_PATH = '../certs/device.pem.crt'
MQTT_KEY_PATH = '../certs/private.pem.key'
MQTT_CA_PATH = '../certs/Amazon-root-CA-1.pem'

TOPIC = 'topic_2'


# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))

# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload.decode()))
    global received_count
    received_count += 1
    if received_count == 3:
        received_all_event.set()
    
mqtt_conn = mqtt_connection_builder.mtls_from_path(
    endpoint = MQTT_BROKER,
    port = MQTT_PORT,
    cert_filepath = MQTT_CERT_PATH,
    pri_key_filepath = MQTT_KEY_PATH,
    ca_filepath = MQTT_CA_PATH,
    on_connection_interrupted = on_connection_interrupted,
    on_connection_resumed = on_connection_resumed,
    keep_alive_secs = 30,
    clean_session = False,
    client_id = 'random_id_123_abc'
    )

print(f"Connecting to {MQTT_BROKER},	topic: {TOPIC}")

future_conn = mqtt_conn.connect()

# results awaits
future_conn.result()
print("Connected")


# Subscribe
print("Subscribing to topic '{}'...".format(TOPIC))
subscribe_future, packet_id = mqtt_conn.subscribe(
        topic=TOPIC,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)

#The shit jaj
message_string = "message"
message = "{} [test]".format(message_string)
payload = json.dumps(message)
print(f"Sending: {payload}")

# Publish some shit
mqtt_conn.publish(
        topic = TOPIC,
        payload = payload,
        qos = mqtt.QoS.AT_LEAST_ONCE
    )

received_all_event.wait()
print("{} message(s) received.".format(received_count))

# Disconnect
print("Disconnecting...")
disconnect_future = mqtt_conn.disconnect()
disconnect_future.result()
print("Disconnected!")
