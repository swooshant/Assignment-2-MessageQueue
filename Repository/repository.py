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
address = "172.31.68.87"
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
        if 'Subject' in data:
            subject = data['Subject']
            if 'Message' in data:
                message = data['Message']
                print("Searching DB")
                result = collection.find({'Subject':{'$regex':subject},'Message':{'regex':message}})
            else:
                print("Searching DB")
                result = collection.find({'Subject':{'$regex':subject}})
        elif 'Message' in data:
            message = data['Message']
            print("Searching DB")
            result = collection.find({'Message':{'$regex':message}})
        print("Sanitizing result")
        for item in list(result):
            item.pop('_id', None)
            myResult.append(item)
        print(myResult)
        reply = json.dumps(myResult)
        ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=reply)
        ch.basic_ack(delivery_tag = method.delivery_tag)

    if data['Action'] == 'push':
        print("Adding to mongodb")
        data.pop('Action', None)
        # Insert the message into the database
        result = collection.insert_one(data)
        ch.basic_ack(delivery_tag = method.delivery_tag)
if __name__ == '__main__':
    gpio.initGPIO()
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.repository
    collection = db.messages

    gpio.lightLED(collection.count())

    desc = {'queue_name': queue_name, 'username': username, 'password': password}
    info = ServiceInfo("_amqp._tcp.local.",
                       "rabbitmq._amqp._tcp.local.",
                       socket.inet_aton(address), port, 0, 0,
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
        gpio.cleanup()
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()

