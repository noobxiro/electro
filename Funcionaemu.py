#!/usr/bin/python

from sense_emu import SenseHat
import datetime
import time
import jwt
import paho.mqtt.client as mqtt
import os
from google.cloud import pubsub_v1
from concurrent import futures

#### VARIABLES PUB/SUB
credentials_path = '/home/pi/Desktop/IoT/colsan-iot-clave.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

topic_path = 'projects/colsan-iot/topics/iotprueba'
subscriber_path = 'projects/colsan-iot/subscriptions/iotsub'

##### vARIABLES CONEXION  IOTCORE(MQTT)
credentials_path = '/home/pi/Desktop/IoT/colsan-iot-clave.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
ssl_private_key_filepath = '/home/pi/Desktop/IoT/rsa_private.pem'
ssl_algorithm = 'RS256' # Either RS256 or ES256
root_cert_filepath = '/home/pi/Desktop/IoT/roots.pem'
project_id = 'colsan-iot'
gcp_location = 'us-central1'
registry_id = 'registro-colsan'
device_id = 'sensor-colsan'


############### START MQTT CONFIG

cur_time = datetime.datetime.utcnow()

def create_jwt():
    token = {
        'iat': cur_time,
        'exp': cur_time + datetime.timedelta(minutes=60),
        'aud': project_id
        }

    with open(ssl_private_key_filepath, 'r') as f:
        private_key = f.read()

    return jwt.encode(token, private_key, ssl_algorithm)

_CLIENT_ID = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, gcp_location, registry_id, device_id)
_MQTT_TOPIC = '/devices/{}/events'.format(device_id)

client = mqtt.Client(client_id=_CLIENT_ID)
# authorization is handled purely with JWT, no user/pass, so username can be whatever
client.username_pw_set(
    username='unused',
    password=create_jwt())

def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))

def on_connect(unusued_client, unused_userdata, unused_flags, rc):
    print('on_connect', error_str(rc))

def on_publish(unused_client, unused_userdata, unused_mid):
    print('on_publish')

client.on_connect = on_connect
client.on_publish = on_publish

client.tls_set(ca_certs=root_cert_filepath) # Replace this with 3rd party cert if that was used when creating registry
client.connect('mqtt.googleapis.com', 8883)
client.loop_start()

############ END MQTT CONFIG


sense = SenseHat()

while True:

    fecha_ini = datetime.datetime.now()
    fecha = fecha_ini.strftime(" %Y/%B/%d - %H:%M:%S")
    hora = fecha_ini.strftime("%H:%M:%S")
###Toma de datos
    Temperatura = sense.get_temperature()
    Presion = sense.get_pressure()
    Humedad = sense.get_humidity()
    
    Temp = round(Temperatura, 1)
    Pres = round(Presion, 1)
    Hum = round(Humedad, 1)
    
    T = str(Temp)
    P = str(Pres)
    H = str(Hum)
  
  
    if T is not None and P is not None and H is not None:

        payload = '{{********* "Fecha": {}************\n"Temperatura": {}, "Presión": {}, "Humedad": {} }}'.format(fecha,T, P, H)

        print("{}\n".format(payload))   

    else:
        print("ERROR, revise el sensor")
    
   

#///////////////FIN PROGRAMACION DISPOSIVITO\\\\\\\\\\\\\\\\\\
    
###### START CONFIG PUB/SUB
  
    publisher = pubsub_v1.PublisherClient()
    topic_path = 'projects/colsan-iot/topics/iotprueba'
    
    data = fecha ## cuerpo del mensaje enviado a pub/sub
    data = data.encode('utf-8')
    attributes = {
        'Temperatura': T,
        'Humedad': H,
        'Presion': P,
        }
    
    future = publisher.publish(topic_path, data, **attributes)
    print(f'published message id {future.result()}')
    
    time.sleep(60)
        