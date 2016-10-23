# Assignment-2-MessageQueue

Packages Required: RabbitMq, MongoDB, and Pika.

Python Libraries: zeroconf, json, pymongo, sys, GPIO, and socket.

Necessary Configuration: 
	Both Pi's need to run sudo hciconfig hci0 piscan && sudo hciconfig hci0 up
	The client and repository Pi's both need mongoDB started
	The repository Pi also needs RabbitMQ started
	Need to run scripts in order of Repository -> Bridge -> Client

Due to issues with Eduroam, the zeroconf portion of the project is commented.
In bridge.py and repository.py there is code that needs to be changed. 
Bridge.py - uncomment the zerconf lines and comment hardcoded values. If not using zerconf, need to change address to repo ip.
Repository.py - change host address to current ip address

Mobile.py - Client
Bridge.py - Bridge
Repository.py - Repository
	+gpio.py is imported into the Repository.py
 		+This includes the code to run the gpio showing the message count

Sample client command: sudo python3 mobile.py -a "push" -s"sample1" -m"sample message"
sample bridge command: sudo python3 bridge.py
sample repository command: sudo python3 repository.py




