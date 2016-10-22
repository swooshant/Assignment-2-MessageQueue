#!/usr/bin/python3

import socket
import sys
from time import sleep

from zeroconf import ServiceInfo, Zeroconf

if __name__ == '__main__':
    desc = {'queue_name': 'myQueue'}

    info = ServiceInfo("_amqp._tcp.local.",
                       "repository._amqp._tcp.local.",
                       socket.inet_aton("127.0.0.1"), 5672, 0, 0,
                       desc, "repository.local")

    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()

