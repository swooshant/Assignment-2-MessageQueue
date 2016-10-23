import json
import pika
import socket
import sys
import uuid

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

class BridgeRpcClient(object):
    def __init__(self):
        print("Setup Rabbitmq connection")
        self.credentials = pika.PlainCredentials('team16', 'ece4564')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('172.31.61.87',
                                                                             5672,
                                                                             '/',
                                                                             self.credentials))

        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, blueData, action):
        if action == "pull":
            self.response = None
        else:
            self.response = "notNone"
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='brogrammers',
                                   properties=pika.BasicProperties(
                                        reply_to = self.callback_queue,
                                        correlation_id = self.corr_id),
                                   body=blueData)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

#bluetooth setup
hostMACAddress = 'B8:27:EB:39:1B:2A' 
port = 25
backlog = 10
size = 4096

#bluetooth
print("Setting up bluetooth socket")
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)

# Setup rpc client
bridgeRPC = BridgeRpcClient()

try:
    while 1:
        print("Get a  bluetooth connection from client")
        client, address = s.accept()

        #blueData is bluetooth data
        print("Recieve bluetooth data")
        blueData = client.recv(size)

        if blueData:
            print(blueData)

            #dictionary of the JSON sent through bluetooth
            data = json.loads(blueData.decode())

            if data['Action'] == "push":
                print("This is a push")
                response = bridgeRPC.call(blueData, "push")
                print(response)
            elif data['Action'] == "pull":
                print("This is a pull")
                response = bridgeRPC.call(blueData, "pull")
                print(response)
                client.send(response)
            else:
                client.send("Invalid Data Sent")

        client.close()

except KeyboardInterrupt:
	print("Closing socket and channel")
	s.close()
	bridgeRPC.connection.close()
