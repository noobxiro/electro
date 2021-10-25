
from sense_emu import SenseHat #emulador sensor T°,Presion y humedad de Raspberry 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import time

#Conexion con Firestore

cred = credentials.Certificate('/home/pi/Desktop/firepi/cred.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


#prueba de nombre para documento
formato1 = (" %Y-%B/%d/%H:%M:%S")
formato2 = ("%H:%M:%S")


sense = SenseHat()

while True:
    fecha_ini = datetime.datetime.now()
    fecha = fecha_ini.strftime(formato1)
    hora = fecha_ini.strftime(formato2)
###Toma de datos
    Temp = sense.get_temperature()
    Pres = sense.get_pressure()
    Hum = sense.get_humidity()
    
    T = round(Temp, 1)
    P = round (Pres, 1)
    H = round (Hum, 1)

    print(fecha)
    print('Temperatura:',T,'°C   Presion:',P, 'mbar   humedad:',H,'%' )
    

### Creador de campo en firestore
    
    data = {
        hora: {
            u'Temperatura (°C)': T,
            u'Humedad (%)': H,
            u'Fecha': datetime.datetime.now()
                      }
        }

    data2 = {
        hora: {
            u'Presión (mbar)': P,
            u'Fecha': datetime.datetime.now()
                  }
        }

####Creador de coleccion y documento en firesotre

#doc_ref = db.collection('mediciones').add(data) # crea un documento con ID random

#Crea coleccion y documento relacion a la temperatura y humedad
    doc_ref = db.collection('Temp y hum').document(fecha)
    doc_ref.set(data)

#Crea coleccion y documento relacion a la Presion
    doc_ref = db.collection('Presion').document(fecha)
    doc_ref.set(data2)  

    time.sleep(30)

    