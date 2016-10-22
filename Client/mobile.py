#!/usr/bin/python3

import json
import sys
import time

from argparse import ArgumentParser

def main(opt_args):
    MsgInst = {}
    # Check some info about the command and build a dictionary for a given action
    if opt_args.action == 'push':
        MsgInst['Action'] = opt_args.action
        MsgInst['MsgID'] = "16" + "$" + str(time.time())
        # Check that both a message and subject have been set for the 'push' action
        if opt_args.subject is None or opt_args.message is None:
            print("The push action requires both a message and a subject")
            sys.exit(1)
        # If both options are set then make them local variables
        else:
            MsgInst['Subject'] = opt_args.subject
            MsgInst['Message'] = opt_args.message
    else:
        MsgInst['Action'] = opt_args.action
        # Check which fields have been set for the 'pull' action
        # Make them local variables if they're set 
        if opt_args.subject is None and opt_args.message is None:
            print("The pull action requires either a message, a subject, or both")
            sys.exit(1)
        if opt_args.subject is not None:
            MsgInst['Subject'] = opt_args.subject
        if opt_args.message is not None:
            MsgInst['Message'] = opt_args.message

    # Conver the MsgInst dictionary into a json payload to be sent to the bridge
    MsgInstJson = json.dumps(MsgInst)
    print(MsgInstJson)
    
    
if __name__ == "__main__":
    parser = ArgumentParser(description='Parse options for the Message Repository')
    parser.add_argument('-a', dest='action', required=True, choices=['push', 'pull'])
    parser.add_argument('-s', dest='subject')
    parser.add_argument('-m', dest='message')
    opt_args = parser.parse_args()

    # execute only if run as a script
    main(opt_args)

