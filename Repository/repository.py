#!/usr/bin/python3

import json
import pymongo
import pika
import socket
import sys
import gpio
from time import sleep

from zeroconf import ServiceInfo, Zeroconf
username = "team16"
password = "ece4564"
address = "172.31.61.87"
port = 5672
queue_name = "brogrammers"

def on_request(ch, method, props, body):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.repository
    collection = db.messages
    myResult = []

    print(" [x] Received %r" % body)
    data = json.loads(body.decode())
    print(data)

    if data['Action'] == 'pull':
        print("pulling")
        if 'Subject' in data and 'Message' in data:
            subject = data['Subject']
            messsage = data['Message']
            print("Searching DB")
            result = collection.find({'Subject':{'$regex':subject},'Message':{'$regex':message}})
        elif 'Subject' in data:
            subject = data['Subject']
            print("Searching DB")
            result = collection.find({'Subject':{'$regex':subject}})
        elif 'Message' in data:
            message = data['Message']
            print("Searching DB")
            result = collection.find({'Message':{'$regex':message}})
        else:
            print("Shouldnt happen, EVER!")
        print("Sanitizing result")
        for item in list(result):
            item.pop('_id', None)
            myResult.append(item)
        reply = json.dumps(myResult)
        print(reply)
        ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=reply)
        ch.basic_ack(delivery_tag = method.delivery_tag)
    elif data['Action'] == 'push':
        print("Adding to mongodb")
        data.pop('Action', None)
        # Insert the message into the database
        result = collection.insert_one(data)
        gpio.lightLED(collection.count())
        ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == '__main__':
    # Setup GPIO
    gpio.initGPIO()
    # Setup MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.repository
    collection = db.messages
    # Setup Zeroconf
    desc = {'queue_name': queue_name, 'username': username, 'password': password}
    info = ServiceInfo("_amqp._tcp.local.",
                       "rabbitmq._amqp._tcp.local.",
                       socket.inet_aton(address), port, 0, 0,
                       desc, "rabbitmq-server.local.")
    # Start Zeroconf
    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)
    # Connect to RabbitMQ
    credentials = pika.PlainCredentials(username=username, password=password)
    connection =  pika.BlockingConnection(pika.ConnectionParameters(host=address,
                                                                    port=port,
                                                                    credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='brogrammers')
    # Begin listening to queue
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='brogrammers')
    print(' [*] Waiting for messages. To exit press CTRL+C')
    # Start consuming messages
    channel.start_consuming()

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        gpio.cleanup()
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()

