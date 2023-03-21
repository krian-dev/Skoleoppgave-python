#Python Server SOCK_STREAM

from threading import Thread
import socket, os, time, sys, traceback, string, json

Conn=0
CThreads={}
Error=""
BError=""

# The seperator used for commands sent
# Eg. if MsgSep = "|", then the text that you must send for a username change will be "UNAME|My name"
MsgSep="|"
svar =  [{"7" : 0, 
            "11" : 1, 
            "5" : 0, 
            "4" : 0,
            }, {"11" : 0, 
            "12" : 0, 
            "13" : 1, 
            "14" : 0,
            }, {"Nilen" : 1, 
            "Amazonas" : 0, 
            "Norske elva" : 0, 
            "Niagra falls" : 0,
            }, {"Sverige" : 1, 
            "Russland" : 0, 
            "Norge" : 0, 
            "New Zealand" : 0,
            }, {"Liverpool" : 1, 
            "Stockholm" : 0, 
            "London" : 0, 
            "New York" : 0,
            }, {"The Dark Side of the Moon" : 1, 
            "The Wall" : 0, 
            "Division Bells" : 0, 
            "A New Meaning Of Life" : 0,
            }, { "Snø-hvit" : 1, 
            "Trollmannen av Oz" : 0, 
            "Mikke Mus og dampbåten Willy" : 1, 
            "Charlie Chaplin klatrer på tak" : 0,
            }, { "Nikelodeon" : 0, 
            "NikeShoes" : 0, 
            "Blue Ribbon Sports" : 1, 
            "Athletesports" : 0,
            }, { "Richard Penicilin" : 0, 
            "Adam Penicilin" : 0, 
            "Alexander Flemming " : 1, 
            "Alexander Biotika" : 0,
            }, { "Antananarivo" : 1, 
            "Madrid" : 0, 
            "Bangui" : 0, 
            "N'Djamena" : 0,
            }, { "Keanu Reeves" : 0, 
            "Morgan Freeman" : 1, 
            "James Whitmore" : 0, 
            "William Sadier" : 0,
            }]
spørsmål = ["Hvor mange tidssoner har Russland??", "Hvor mange striper inneholder flagget til USA?","Hva heter verdens lengste elv?", "Hvilket land inneholder flest øyer?", "Hvilken by kommer The Beatles fra?", "Hva heter Pink Floyd sitt mest-selgende album?", "Hva het Disney sin første film?", "Hva het nike før de skiftet navn?" "Hvem Oppdagde et av de første anti-biotikane: Pnicilin?", "Hva heter hovedstaden i Madagascar?" 'Hvem spillte karakteren Red i "The Shawshank redemption"?', ]
print(svar)

ip="localhost"
port=27000

server_socket=None


#________________________________________________________________________________________________________________
#SERVERTHREAD: UID 0
# This class consists of the thread used for the server. This will listen for all new connections and spawn new "Client-threads" for each one that connects.
class server(Thread):
    def __init__(self, ip=ip, port=port):
        Thread.__init__(self)
        self.name = ip+":"+str(port)
        self.alive=True
        self.CList={}
        self.CTLock=False

    def broadcast(self, Str):
        # Send a command to all connected clients 
        for x in CThreads:
            CThreads[x].send(Str)

    def broadcastMSG(self, From, UID, Mesg):
        # Send a message to all connected clients 
        for x in CThreads:
            if not str(x)==str(UID):
                CThreads[x].MESG(str(UID),Mesg)

    def UpdateCList(self):
        # Updates list of connected clients 
        self.CList={}
        for x in CThreads:
            self.CList[x]={}
            self.CList[x]["UID"]=CThreads[x].UID
            self.CList[x]["Uname"]=CThreads[x].Uname

    def UpdateCThreads(self):
        # Updates list of connected client threads, checks if any dead threads needs to be cleaned up
        if self.CTLock==False:
            self.CTLock=True
            DeadThreads={}
            for x in CThreads:
                if not CThreads[x].is_alive():
                    DeadThreads[x]=CThreads[x]
                    print("Removing dead thread: "+str(x))
                    self.broadcast("DCONN"+MsgSep+str(CThreads[x].UID)+MsgSep+CThreads[x].state)
            for x in DeadThreads:
                del CThreads[x]
            self.UpdateCList()
            self.CTLock=False

    def Crash(self):
        # Tests the exception handler
        raise Exception("crashtest")

    def run(self):
        # Mainloop, accepts connections and spawns client threads. 
        global Conn, CThreads, Error, LastConn
        print(str(self))
        while self.alive:
            try:
                # print("Accepting Connections...")
                channel, details = server_socket.accept()
                print("Client connected "+ str(details))
                Conn+=1
                CThreads[Conn]=client(channel,Conn)
                CThreads[Conn].state="Starting"
                CThreads[Conn].start()
                CThreads[Conn].name = details
                self.UpdateCThreads()
                LastConn=Conn
                if self.alive==False:
                    print("I should be dead.. :(")

            except socket.timeout:
                pass

            except socket.error as e:
                SError=e
                print(str(e))
                self.alive=False
        if self.alive==False:
            print("Server stopped..")

#________________________________________________________________________________________________________________
#CLIENTTHREAD: UID1-inf
# This class consists of the thread used for a client. This keeps track of the client state and handles communication to and from it.
class client(Thread):
    def __init__ (self, channel,UID):
        Thread.__init__(self)
        self.channel=channel
        self.alive=True
        self.UID=UID
        self.Uname="N/A"
        self.state="START"
        self.runde= 0
        self.ferdig= 0

    def send(self, msg):
        # Sends a command/message to the client
        try:
            self.channel.send(bytes(msg, "UTF-8"))
        except socket.error as e:
            lasterror=e
            print("Failed to send message, client: "+str(self.UID)+" lost connection?")
            self.state="FAILEDSEND"
            self.alive=False

    def ping(self):
        # Sends the text "PING" to the client, and counts the time it takes before receiving one back, see self.pong under run(self).
        try:
            self.channel.send(bytes("PING", "UTF-8"))
            self.pong=None
            timeout=time.time()+10
            while self.pong==None:
                if time.time()>timeout:
                    self.pong=False
                pass
            if self.pong==True:
                return time.time()-(timeout-10)
            else:
                return False
        except socket.error as e:
            print(e)
            Error=e
            return False

    def MESG(self, uid, msg):
        # Sends a text message to the client
        self.send("MESG"+MsgSep+str(uid)+MsgSep+msg)

    def run(self):
        # Main functions for the client
        global Error, BError

        # Try to send the client it's UID number when it initially connects.
        # This runs at once when a client has connected
        try:
            self.send("UID"+MsgSep+str(self.UID))
            self.poeng = 0 ######
            
        except socket.error as e:
            error=e
            print("Failed to initialize UID "+str(self.UID))
            self.state="INITFAIL"
            self.alive=False
        
        # The client thread mainloop, listens for and handles all incoming messages from the client
        while self.alive:
            try:
                data=self.channel.recv ( 200 ).decode()
                datasplit=data.rstrip().split(MsgSep)
                command=datasplit[0]
                BError=data
                if not data:
                    print("Client disconnected: "+str(self.channel.getsockname()))
                    self.alive=False
                    self.state="DCONN"
                else:
                    if command=="MESG":
                        print(str(self.UID)+":"+datasplit[1])
                        self.channel.send(bytes("RECV"+MsgSep, "UTF-8"))
                        ServerListener.broadcastMSG("USER",str(self.UID),datasplit[1])

                    elif command=="UNAME":
                        print("User: "+self.Uname+": "+str(self.UID)+"changed name to: "+datasplit[1])
                        self.Uname=datasplit[1]
                        ServerListener.UpdateCList()
                        ServerListener.broadcast("UNAME"+MsgSep+str(self.UID)+MsgSep+self.Uname)

                    elif command=="crash":
                        a=a+1

                    elif command=="PING":
                        print("Ping recived from "+str(self.UID))
                        self.pong=True
                    
                    elif command=="spm":
                        if self.runde == len(spørsmål):
                            for x in CThreads:
                                self.send((CThreads[x].Uname + ": " + str(CThreads[x].poeng)+'\n'))
                                if self.ferdig == 0:
                                    time.sleep(1)
                                    self.send("Ferdig")
                                    self.ferdig = 1
                        else:
                            self.ferdig = 0
                            self.send(spørsmål[self.runde]+"\n")
                            for i in range(len(svar[self.runde])):
                                print(i)
                                #self.send (("%s) %s" % (string.ascii_uppercase[i], list(svar.keys().encode('UTF-8')[i]))))
                                self.send(string.ascii_uppercase[i] + ") " + list(svar[self.runde].keys())[i] + "\n")
                            self.send('Hva tror du?'+"\n")
                    
                    elif command=="answer":
                        if self.ferdig == 0:
                            svaret_ditt = datasplit[1].upper()
                            svaret_ditt = (string.ascii_uppercase.index(svaret_ditt))
                            svaret_ditt = list(svar[self.runde].keys())[svaret_ditt]
                            
                                            
                            if svar[self.runde][svaret_ditt] == 1:
                                self.send (" Bra jobba, du fikk rett"+'\n')
                                self.poeng = self.poeng + 1
                                self.runde=self.runde+1
                            else:
                                self.send (" Du fikk feil"+'\n')
                                self.runde=self.runde+1
                            

                    else:
                        print("UNDEFINED RESPONSE FROM UID"+str(self.UID)+": "+data)

            except socket.error as e:
                pass
            except IndexError as e:
                print("Bad behaviour from: "+str(self.UID)+" : "+str(self.name))
                traceback.print_exc()
            except:
                print("Client "+str(self.UID)+" crashed: "+str(sys.exc_info()[0])[18:])
                ServerListener.UpdateCThreads()
                traceback.print_exc()
                self.alive=False

        if self.alive==False:
            ServerListener.UpdateCThreads()
            pass



# Configure the networking sockets for the server
def Bootup():
    global server_socket, ServerListener, ip, port
    print("Starting up...")
    server_socket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind ( ( ip, port ) )
    server_socket.settimeout(1)
    server_socket.listen(5)
    print("Listening...")
    ServerListener=server(ip, port)
    ServerListener.start()

Bootup()

#_____________________________________________________________________________________________________________________
#Server console commands

Malive=True
while Malive:
    arg=input()
    ServerListener.UpdateCThreads()
    
    try:
        ComPar=arg.split(" ")
        Command=ComPar[0]
        
        if Command=="ls":
            print("UID TYPE      IP          PORT    STATE   TID")
            for x in CThreads:
                print(str(x)+" "*(3-len(str(x)))+":"+str(CThreads[x]))

        elif Command=="killinactive":
            print("Killing inactive client threads")
            ServerListener.UpdateCThreads()

        elif Command=="clist":
            print("CLI:    Info:")
            for x in ServerListener.CList:
                print(ServerListener.CList[x])
                
        elif Command=="poeng":
            for x in CThreads:
                print(CThreads[x].Uname + ": " + str(CThreads[x].poeng))
        
        elif Command=="clistupd":
            print("Updating Client List...")
            ServerListener.UpdateCList()

        elif Command=="crashtest":
            raise Exception("crashtest")

        elif Command=="restart":
            print("Shutting down...")
            for x in CThreads:
                print("Disconnecting Client: "+CThreads[x].name)
                CThreads[x].channel.close()
                CThreads[x].alive=False

            print("Killing server thread: "+ServerListener.name)
            ServerListener.alive=False
            server_socket.close()

            #Startup process
            print("Booting up..")
            Bootup()
            print("Reboot complete")

        elif Command=="send":
            try:
                if int(ComPar[1]) in CThreads:
                    foo=""
                    for x in ComPar:
                        if not x=="send" and x!=ComPar[1]:
                            foo=foo+x+" "
                    CThreads[int(ComPar[1])].send(foo)
            except ValueError as e:
                Error=e
                print("send must be used with an userid")

        elif Command=="broadcast":
            try:
                foo=""
                for x in ComPar:
                    if not x=="broadcast":
                        foo=foo+x+" "
                ServerListener.broadcast(foo)
            except ValueError as e:
                Error=e
                print("broadcast failed")

        elif Command=="ping":
            try:
                if int(ComPar[1]) in CThreads:
                    print("Pinging: UID"+ComPar[1]+" | "+CThreads[int(ComPar[1])].name)
                    fooping=CThreads[int(ComPar[1])].ping()
                    if fooping:
                        print("Pinging successful, time taken: "+str(fooping))
                    else:
                        print("Client refused to respond to ping in time")
                else:
                    print("User ID: "+ComPar[1]+" does not exsist")
            except ValueError as e:
                Error=e
                print("Ping must be used with an user id (UID)")

        elif Command=="exit":
            print("Shutting down...")
            for x in CThreads:
                print("Disconnecting Client: "+CThreads[x].name)
                CThreads[x].channel.close()
                CThreads[x].alive=False

            print("Killing server thread: "+ServerListener.name)
            ServerListener.alive=False
            server_socket.close()

            print("Killing mainloop")
            Malive=False

        elif Command=="lasterror":
            print(Error)

        elif Command=="berror":
            print(BError)

        elif Command=="traceback":
            print(traceback.format_exc())
        
        elif Command=="kick":
            try:
                if int(ComPar[1]) in CThreads:
                    print("Kicking: UID"+ComPar[1]+" | "+CThreads[int(ComPar[1])].name)
                    reason=""
                    for x in ComPar:
                        if not (x=="kick" or x==str(ComPar[1])):
                            reason=reason+x+" "
                    ServerListener.broadcast("KICK"+MsgSep+ComPar[1]+MsgSep+reason)
                    CThreads[int(ComPar[1])].alive=False
                    del CThreads[int(ComPar[1])]
                    ServerListener.UpdateCList()
                else:
                    print("User ID: "+ComPar[1]+" does not exsist")
            except ValueError as e:
                Error=e
                print("Kick must be used with an user id (UID)")
    
        elif Command=="say":
            stri=""
            for x in ComPar:
                if not x=="say":
                    stri=stri+x+" "
            ServerListener.broadcastMSG("SERVER",0,stri)

        elif Command=="clear":
            os.system("clear")

        elif Command=="":
            pass

        else:
            print("Command *"+Command+"* not found")
            
    except RuntimeError as e:
        pass
