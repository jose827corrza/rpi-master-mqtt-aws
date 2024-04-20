from awsiot import mqtt_connection_builder

MQTT_BROKER = 'a1gtemfhsymp11-ats.iot.us-east-1.amazonaws.com'
MQTT_PORT = 8883
MQTT_CERT_PATH = '../certs/device.pem.crt'
MQTT_KEY_PATH = '../certs/private.pem.key'
MQTT_CA_PATH = '../certs/Amazon-root-CA-1.pem'

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))

# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))
    

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


#Connect
def mqtt_connect():
    future_conn = mqtt_conn.connect()
    # results awaits
    future_conn.result()
    print("Connected")


# Disconnect
def mqtt_disconnect():
    print("Disconnecting...")
    disconnect_future = mqtt_conn.disconnect()
    disconnect_future.result()
    print("Disconnected!")