#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
from bluetooth import *

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)
