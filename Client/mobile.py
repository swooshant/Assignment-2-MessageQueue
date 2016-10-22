#!/usr/bin/python3

import json
import pymongo
import socket
import sys
import time

from argparse import ArgumentParser

def main(opt_args):
    # Setup some bluetooth stuff
    bridgeMAC = 'B8:27:EB:39:1B:2A'
    bridgePort = 25
    bridgeSocket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    bridgeSocket.connect((bridgeMAC, bridgePort))

    # Initialize DB related stuff
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.repository
    collection = db.messages

    # Create a dict to represetnt the message to be sent over bluetooth
    payload = {}

    # Check some info about the command and build a dictionary for a given action
    if opt_args.action == 'push':
        # Set some of the fields of the payload
        payload['Action'] = opt_args.action
        payload['MsgID'] = "16" + "$" + str(time.time())
        # Check that both a message and subject have been set for the 'push' action
        if opt_args.subject is None or opt_args.message is None:
            print("The push action requires both a message and a subject")
            sys.exit(1)
        # If both options are set then make them local variables
        else:
            payload['Subject'] = opt_args.subject
            payload['Message'] = opt_args.message
    else:
        payload['Action'] = opt_args.action
        # Check which fields have been set for the 'pull' action
        # Make them local variables if they're set 
        if opt_args.subject is None and opt_args.message is None:
            print("The pull action requires either a message, a subject, or both")
            sys.exit(1)
        if opt_args.subject is not None:
            payload['Subject'] = opt_args.subject
        if opt_args.message is not None:
            payload['Message'] = opt_args.message

    # Convert payload dict to a json opject
    payloadJSON = json.dumps(payload)
    print(payloadJSON)

    # Insert the message we'll be sending into the database
    result = collection.insert_one(payload)

    # Send json message to the bridge
    bridgeSocket.send(bytes(payloadJSON, 'UTF-8'))
    bridgeSocket.close()
        
if __name__ == "__main__":
    parser = ArgumentParser(description='Parse options for the Message Repository')
    parser.add_argument('-a', dest='action', required=True, choices=['push', 'pull'])
    parser.add_argument('-s', dest='subject')
    parser.add_argument('-m', dest='message')
    opt_args = parser.parse_args()

    # execute only if run as a script
    main(opt_args)

