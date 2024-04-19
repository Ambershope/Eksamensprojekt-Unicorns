'''
Networking script for sending and reciving messages in our game.\n
To start Create a NetConnecter objekt, this objekt will hold all networking processes
'''

import socket
import threading
from time import sleep


class NetConnecter():
    '''
    This class handels Networking in our game, \nHere we can open ports and connect to ports on certain addresses
    '''
    def __init__(self, port = 36563):
        self.port = port
        self.socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.stopServer = False
        self.client = None
        self.cliAddr = None
        self.addr = (socket.gethostbyname(socket.gethostname()), self.port)
        self.addrUDP = ('224.0.2.60', 34543)
        self.timeToLive = 2   # Router Jump Points Allowed
        self.broadcastingUDP = True
        self.listerUDP = True
        self.openServers = []
        self.serverName = str(self.addr[0] + ":" + str(self.addr[1]))

    # ----------   General functions   ----------
    


    # ----------   UDP Port functions   ----------
    def broadcastServer(self):
        '''
        This function starts a TCP server and then broadcast the ip, for this computer.\n
        This allows other computers on the same internet to find this server.\n
        '''
        print("Server starting to broadcast")
        threading.Thread(target=self.openTCPPort).start()
        self.broadcastingUDP = True
        self.socketUDP.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.timeToLive)
        threading.Thread(target=self.broadcastServerTreadUDP).start()

    def broadcastServerTreadUDP(self):
        '''
        This function should not be called, except as a thread. \n
        To turn of set broadcastingUDP to false. \n
        It is part of broadcastServer, and will crash the program if called.
        '''
        while self.broadcastingUDP:
            print(str("O:" + self.addr[0] + ":" + str(self.addr[1])))
            self.socketUDP.sendto(str("O:" + self.addr[0] + ":" + str(self.addr[1]) + ":" + self.serverName).encode("utf-8"), self.addrUDP)
            sleep(1.5)
        self.socketUDP.sendto(str("C:" + self.addr[0] + ":" + str(self.addr[1]) + ":" + self.serverName).encode("utf-8"), self.addrUDP)

    def serverLister(self):
        '''
        This function lists servers open, servers need to broadcast that they are open before they are listed.\n
        If this function is called multiple times it prints 'Server already listening'.\n
        To find / use the list, it is stored in openServers.
        '''
        try:
            self.listerUDP = True
            self.socketUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try: self.socketUDP.bind(('', self.addrUDP[1]))
            except: pass
            mreq = socket.inet_aton(self.addrUDP[0]) + socket.inet_aton('0.0.0.0')
            self.socketUDP.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            print("Server starting to listen")
            threading.Thread(target=self.serverListerTreadUDP).start()
        except:
            print("Server already listening")
    
    def serverListerTreadUDP(self):
        '''
        This function should not be called, except as a thread. \n
        To turn of, run leaveServerLister \n
        It is not recommended to turn of the thread by setting listerUDP to false \n
        It is part of serverLister, and will crash the program if called.
        '''
        while self.listerUDP:
            message = self.socketUDP.recv(1024).decode('utf-8')
            print(message)
            message = message.split(':')
            if message[0] == 'O':
                addr = (message[1], message[2])
                if addr not in self.openServers: self.openServers.append((addr, message[3]))
            print(self.openServers)
            if message[0] == 'C':
                addr = (message[1], message[2])
                try: self.openServers.remove((addr, message[3]))
                except: pass
    
    def leaveServerLister(self):
        '''
        This command stops the server from listing servers.\n
        Nothing happens if the program is not listing servers.
        '''
        try:
            self.openServers = []
            self.listerUDP = False
            mreq = socket.inet_aton(self.addrUDP[0]) + socket.inet_aton('0.0.0.0')
            self.socketUDP.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
        except: pass # This code will run if the lister is ofline.
        print("Server stopped listening")


    # ----------   TCP Port functions   ----------
    def sendTCPMessage(self, message):
        pass

    def resiveTCPMessage(self, procesFunk):
        pass

    def openTCPPort(self):
        '''
        This function opens a TCP port on current address, this allows another computer to connect.\n
        This port is only talked throug 1 on 1 channel.\n
        This function should not be used with it self.\n
        '''
        try:
            self.addr = (socket.gethostbyname(socket.gethostname()), self.port)
            self.socketTCP.bind(self.addr)
            print("Server open on", self.addr[0], ":", self.addr[1])
            self.socketTCP.listen()
            self.client, self.cliAddr = self.socketTCP.accept()
            print("Got connection from", self.cliAddr)
        except: print("Server already open!")

    def connectTCPPort(self, portAddress):
        '''
        This function should not be used on your own.
        \nInstead use connect().
        '''
        try:
            self.socketTCP.connect(portAddress)
            print(portAddress, self.port)
        except:
            print("Port not open on", portAddress, ":", self.port)





if __name__ == "__main__":

    netCon = NetConnecter()

    def startClient(addr):
        print("Client is starting")
        netCon.connectTCPPort(addr)
        pass

    def startServer():
        print("Server is starting")
        threading.Thread(target=netCon.openTCPPort).start()
        
    def clientMessage():
        pass

    from tkinter import *
    root = Tk()
    root.title("Networking Test")
    root.geometry("500x120")
    cL = None
    f1 = Frame(root)
    e1 = Entry(f1, width=50, justify=CENTER)
    e1.insert(END, socket.gethostbyname(socket.gethostname()))
    e2 = Entry(f1, width=50, justify=CENTER)
    b1 = Button(f1, text="Start Client", command=lambda: startClient((e1.get()), netCon.port))
    b2 = Button(f1, text="Start 'Server'", command=startServer)
    b3 = Button(f1, text="Find open ports", command=lambda: netCon.serverLister())
    b4 = Button(f1, text="UDP messaging", command=lambda: netCon.broadcastServer())
    b5 = Button(f1, text="Stop finding ports", command=lambda: netCon.leaveServerLister())
    # b3 = Button(f1, text="Find open ports", command=lambda: threading.Thread(target=findPorts, args=()).start())
    l1 = Label(f1, text=" --- Netværks text --- ")
    f1.pack()
    l1.grid(row=0, column=0, columnspan=3)
    b1.grid(row=1, column=0)
    b2.grid(row=1, column=1)
    b3.grid(row=2, column=0)
    b4.grid(row=2, column=1)
    b5.grid(row=2, column=2)
    # b3.grid(row=1, column=2)
    e1.grid(row=3, column=0, columnspan=3)
    e2.grid(row=4, column=0, columnspan=3)
    e2.bind('<Return>', lambda: clientMessage())
    root.mainloop()

''' Code that is no longer used '''

# def connectTest(sock, addr, port):
#     try:
#         sock.connect((addr, port))
#         print("Port " + str(port) + " open on address: " + addr)
#     except:
#         pass


# def findPorts(port=35565):
#     '''
#     Finds a list of open ports on current internet
#     \n*port is the port to search on. Default 35565.
#     '''
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     ipconst = socket.gethostbyname(socket.gethostname()).split(".")
#     ipconst = ipconst[0] + "." + ipconst[1]
#     for i in range(256):
#         for j in range(256):
#             threading.Thread(target=connectTest, args=(sock, ipconst + ".{}.{}".format(i, j), port)).start()
#     pass