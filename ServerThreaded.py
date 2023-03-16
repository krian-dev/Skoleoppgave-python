#Python Client Example
import socket
from threading import Thread
mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Connecting...")

try:
	print(mySocket.connect(("localhost",27000)))
except socket.error as e:
	print(e)
	raw_input()
print("Connected!")
alive=True

class listen(Thread):
	def __init__(self):
		Thread.__init__(self)
	
	def run(self):
		while alive:
			recv=mySocket.recv(100).decode("ascii")
			if recv=="PING":
				print("Ping recived, responding...")
				mySocket.send(b"PING")
			else:
				print(recv)
		if not alive:
			print("Listen is dead")

TListen=listen()
TListen.start()

alive=True
while alive:
	Type=input(">> ")
	print(Type)
	if Type=="exit":
		TListen.alive=False
		mySocket.close()
		alive=False
	else:
		mySocket.send(bytes(Type, "ascii"))

