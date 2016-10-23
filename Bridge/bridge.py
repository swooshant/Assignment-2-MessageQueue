import socket
import sys
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
import pika
import json


hostMACAddress = 'B8:27:EB:39:1B:2A' 
port = 25
backlog = 1
size = 4096

#bluetooth
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)

#messageQueue
credentials = pika.PlainCredentials('team16', 'ece4564')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.31.61.87', 5672, '/', credentials))
channel = connection.channel()
result = channel.queue_declare(exclusive=True)
callback_queue = result.method.queue


def on_response(ch, method, props, body):
	hello = "10"


def call(blueData, res):
		if res == "push":
			response = "notNone"
		elif res == "pull":
			response = None;

		channel.basic_publish(exchange='', routing_key='brogrammers', properties=pika.BasicProperties(
                                         reply_to = callback_queue),
                                   body= blueData)
		while response is None:
			connection.process_data_events()


channel.basic_consume(on_response, no_ack=True, queue=callback_queue)


print("Stage 1")

try:
	while 1:
		client, address = s.accept()

		#blueData is bluetooth data
		blueData = client.recv(size)
		
		if blueData:
			print("stage 2")

			print(blueData)

			#dictionary of the JSON sent through bluetooth
			data = json.loads(blueData.decode())

			if data['Action'] == "push":
				
				print("This is a push")
				call(blueData, "push")
				client.close()

			elif data['Action'] == "pull":
				print("This is a pull")
				call(blueData, "push")

			else:
				print("Invalid Action: Retry")
				client.close()

		else:
			client.send("Invalid Data Sent")
			client.close()

except KeyboardInterrupt:
	print("Closing socket and channel")
	s.close()
	connection.close()

		


