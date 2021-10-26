###EN ESTE CODIGO SOLO SE ESTRAE HUMEDAD Y TEMPERATURA

from google.cloud import firestore
from datetime import datetime

client = firestore.Client(project='NOMBRE PROYETO FIRESTORE')

def pubsub_fire(event, context):
    import base64

    print(f'This function was triggered by messageId {context.event_id}, published at {context.timestamp} to {context.resource["name"]}!')

    message = 'MENSAJE QUE DESEE ENVIAR COMO TITULO O DESCRIPTIVO'
    if 'data' in event:
        message = base64.b64decode(event['data']).decode('utf-8')
    print(f'message: {message}')
    

    try:
        if 'attributes' in event:
            attributes = event['attributes']
            temperatura = attributes['Temperatura']
            humedad = attributes['Humedad']
        
    except Exception as e:
        print(f'error with attributes: {e}')

    

    data1 = {
         message:{
            'Temperatura': temperatura,
            'Humedad': humedad,
                     }
    }
            
        
    doc_id = datetime.now().strftime("%Y/%B-%d/%H:%M:%S")
    doc = client.collection('COLECCION').document(doc_id)   ### EN FIRESTORE SE VERÁ COMO  COLECCION/AÑO/MES-DIA/HORA SERVIDOR (para configurar la hora local puede enviar la hora como un atributo o como message)
    doc.set(data1)


