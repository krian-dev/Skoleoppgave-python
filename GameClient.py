#Python Client Example
import socket
from threading import Thread
mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Connecting...")

MsgSep="|"
Navn = 0
ferdig = 0

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
		global Navn
		global ferdig
		while alive:
			recv=mySocket.recv(1024).decode("UTF-8")
			datasplit=recv.rstrip().split(MsgSep)
			command=datasplit[0]
			if command=="PING":
				print("Ping recived, responding...")
				mySocket.send(b"PING")
			elif command=="UNAME":
				print("Spiller joina: "+ datasplit[2]+'\n')
				Navn = 2
			elif command =="UID":
				print()
			elif command=="Ferdig":
				ferdig=1
				print("Du blei ferdig, bra jobbat")
			else:
				print(recv)
		if not alive:
			print("Listen is dead")

TListen=listen()
TListen.start()

alive=True
while alive:
	if Navn == 0:
		Type=(input("Hva skal du hete?"))
		mySocket.send(bytes("UNAME|"+Type+'\n', "UTF-8"))
		Navn=1
	elif Navn == 1:
		pass
	else:
		mySocket.send(bytes("spm|","UTF-8"))
		Type=input(">> ")
		if Type=="exit":
			TListen.alive=False
			mySocket.close()
			alive=False
		elif ferdig==0:
			mySocket.send(bytes("answer|"+Type, "UTF-8"))
		elif ferdig==1:
			print("Du ble ferdig :) Her er resultatene")
			mySocket.send(bytes(Type, "UTF-8"))

