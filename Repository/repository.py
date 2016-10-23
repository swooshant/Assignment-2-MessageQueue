#!/usr/bin/python3

import json
import pymongo
import pika
import socket
import sys
from time import sleep

from zeroconf import ServiceInfo, Zeroconf

def on_request(ch, method, props, body):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.repository
    collection = db.messages

    print(" [x] Received %r" % body)
    data = json.loads(body.decode())
    print(data)
    if data['Action'] == 'pull':
        print("pulling")
	if data['Subject'] is not None
		subject = data['Subject']
		if data['Message'] is not None
			message = data['Message']
			result = collection.find({'Subject':{'$regex':subject},'Message':{'regex':message}})
			print(result)
		else
			result = collection.find({'Subject':{'$regex':subject})
			print(result)
	elif data['Message'] is not none
		message = data['Message']
		result = collection.find({'Message':{'$regex':message})
		print(result)
    if data['Action'] == 'push':
        print("Adding to mongodb")
        data.pop('Action', None)
        # Insert the message into the database
        result = collection.insert_one(data)
        ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == '__main__':
    desc = {'queue_name': 'myQueue'}
    info = ServiceInfo("_amqp._tcp.local.",
                       "rabbitmq._amqp._tcp.local.",
                       socket.inet_aton("127.0.0.1"), 5672, 0, 0,
                       desc, "rabbitmq-server.local.")

    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)

    credentials = pika.PlainCredentials(username='team16', password='ece4564')
    connection =  pika.BlockingConnection(pika.ConnectionParameters(host='172.31.61.87',
                                                                    port=5672,
                                                                    credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='brogrammers')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='brogrammers')
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()

