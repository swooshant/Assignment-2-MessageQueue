import socket
import sys
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
import pika
import json
import uuid

#bluetooth setup
hostMACAddress = 'B8:27:EB:39:1B:2A' 
port = 25
backlog = 10
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

response = None
corr_id = str()

def on_response(ch, method, props, body):
		print("In on_response: Print Body: ")
		print(body)
		response = body


def call(blueData, action):
		if action == "pull":
			response = None
		else:
			response = "notNone"

		corr_id = str(uuid.uuid4())
		channel.basic_publish(exchange='', routing_key='brogrammers', properties=pika.BasicProperties(
                                         reply_to = callback_queue,   correlation_id = corr_id),
                                   body= blueData)
		while response is None:
			connection.process_data_events()

		return 


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

			elif data['Action'] == "pull":
				print("This is a pull")
				call(blueData, "pull")
				print("In Main: Print Response: ")
				print(response)
				client.send(response)

		else:
			client.send("Invalid Data Sent")

		client.close()
		s.close()

except KeyboardInterrupt:
	print("Closing socket and channel")
	s.close()
	connection.close()

		


