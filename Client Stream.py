#Python Client DGRam
import socket
from threading import Thread
mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Connecting...")
#10.35.36.164
try:
	print(mySocket.connect(("192.168.0.108",27000)))
except socket.error, e:
	print(e)
	raw_input()
print("Connected!")
alive=True

class listen(Thread):
	def __init__(self):
		Thread.__init__(self)
	
	def run(self):
		while alive:
			recv=mySocket.recvfrom(100)
			if recv=="PING":
				print("Ping recived, responding...")
				mySocket.send("PING")
			else:
				print(recv)
		if not alive:
			print("Listen is dead")
TListen=listen()
TListen.start()

alive=True
while alive:
	Type=raw_input("<<")
	print(Type)
	if Type=="exit":
		TListen.alive=False
		mySocket.close()
		alive=False
	else:
		mySocket.send(Type)

