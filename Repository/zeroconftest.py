#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Example of browsing for a service (in this case, HTTP) """

import socket
import sys
from time import sleep

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

if __name__ == '__main__':
    zeroconf = Zeroconf()
    print("\nBrowsing services, press Ctrl-C to exit...\n")
    browser = ServiceBrowser(zeroconf, "_amqp._tcp.", handlers=[on_service_state_change])
    info = zeroconf.get_service_info("_amqp._tcp.local.", "rabbitmq._amqp._tcp.local.")
    print(info)

    zeroconf.close()
