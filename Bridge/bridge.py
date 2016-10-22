import socket

hostMACAddress = 'B8:27:EB:39:1B:2A' 
port = 25
backlog = 1
size = 1024

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)

try:
	client, address = s.accept()
	while 1:
		data = client.recv(size)
		if data:
			print(data)
			client.send(data)
except:
	print("Closing socket")
	client.close()
	s.close()