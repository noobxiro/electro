

from google.cloud import firestore
from datetime import datetime

client = firestore.Client(project='colsan-iot')

def pubsub_fire(event, context):
    import base64

    print(f'This function was triggered by messageId {context.event_id}, published at {context.timestamp} to {context.resource["name"]}!')

    message = 'fecha'
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
            
        
    doc_id = datetime.now().strftime("%Y-%B/%d/")
    doc = client.collection('Raspberry pi').document(message)
    doc.set(data1)


