from http.server import BaseHTTPRequestHandler, HTTPServer
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import hmac
import requests
import hashlib
import json
import os
import base64

legacy_pos_webhook = False
shared_secret = b'cdQ-Xk6wJ0BeVSX9c4JPQJOhVwa9uvQjHuiewvfozPXMTEV4FW9vG0zG0EcLZdS8J_BqqdT5GduM_wG-kdd12g'
url = "https://api-sandbox.developers.deliveroo.com/order/v1/deliveroo/order-events"



# Initialize Firebase credentials
cred = credentials.Certificate("/etc/secrets/credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()



class DeliverooHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        sequence = self.headers.get('x-deliveroo-sequence-guid')
        expected = self.headers.get('x-deliveroo-hmac-sha256')

        hmac_calculator = hmac.new(shared_secret, digestmod=hashlib.sha256)
        hmac_calculator.update(sequence.encode())

        if legacy_pos_webhook:
            hmac_calculator.update(b' \n ')
        else:
            hmac_calculator.update(b' ')

        content_length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_length)
        hmac_calculator.update(body)

        calculated = hmac_calculator.hexdigest()

     

        if expected != calculated:
            self.send_response(400)
        else:
            self.send_response(200)
          


        self.end_headers()
        print("Response sent to the server:")
        print(body.decode())
        data = json.loads(body.decode())
        location_id = data['body']['order']['location_id']
        event = data['event']
        print("Store ID:", location_id)
        read_field("Stores", "Store ID", location_id, body.decode(), event)


       

def run(server_class=HTTPServer, handler_class=DeliverooHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting http on port {port}...')
    httpd.serve_forever()


def read_field(collection_name, document_id, field_name, data, event):
    # Get a reference to the Firestore database
    db = firestore.client()

    # Get the document snapshot
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()

    if event == "order.new":
    
        print("New order has arrived!")
       



 
    
    

   

# Call the function with your desired collection name, document ID, and field name


if __name__ == '__main__':
    run()
