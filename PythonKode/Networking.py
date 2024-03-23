'''
Networking script for sending and reciving messages in our game.\n
To start Create a NetConnecter objekt, this objekt will hold all networking processes
'''

import socket
import threading
import time


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
        self.addr = None
        self.addrUDP = ('224.0.2.60', 34543)
        self.timeToLive = 2   # Router Jump Points Allowed
        self.broadcastingUDP = True
        self.openServers = []


    # ----------   UDP Port functions   ----------
    def broadcastServer(self):
        print("Server starting to broadcast")
        self.socketUDP.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.timeToLive)
        self.broadcastingUDP = True
        threading.Thread(target=self.broadcastServerTreadUDP)

    def broadcastServerTreadUDP(self):
        '''
        This function should not be called, except as a thread. \n
        To turn of set broadcastingUDP to false. \n
        It is part of broadcastServer, and will crash the program if called.
        '''
        while self.broadcastingUDP:
            self.socketUDP.sendto("I am open :)".encode("utf-8"), self.addrUDP)
            time.sleep(1.5)

    def serverLister(self):
        print("Server starting to listen")
        self.socketUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socketUDP.bind(('', self.addrUDP[1]))
        mreq = socket.inet_aton(self.addrUDP[0]) + socket.inet_aton('0.0.0.0')
        self.socketUDP.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        threading.Thread(target=self.serverListerTreadUDP)
    
    def serverListerTreadUDP(self):
        while True:
            print(self.socketUDP.recv(1024))
            pass
    
    def leaveServerLister(self):
        mreq = socket.inet_aton(self.addrUDP[0]) + socket.inet_aton('0.0.0.0')
        self.socketUDP.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
        print("Server stopped listening")


    # ----------   TCP Port functions   ----------
    def sendTurn(self, message):
        pass

    def resiveTurn(self, processFunk):
        pass

    def openTCPPort(self):
        '''
        This function opens a TCP port on current address, this allows another computer to connect.\n
        This port is only talked throug 1 on 1 channel.\n
        This function should not be used with it self.\n
        '''
        addr = (socket.gethostbyname(socket.gethostname()), self.port)
        self.socketTCP.bind(addr)
        print("Server open on", addr[0], ":", addr[1])
        self.socketTCP.listen()
        self.client, self.addr = self.socketTCP.accept()
        print("Got connection from", self.addr)

    def connectTCPPort(self, portAddress, port = 35565):
        '''
        This function should not be used on your own.
        \nInstead use connect().
        '''
        try:
            self.socketTCP.connect((portAddress, port))
            print(portAddress, port)
        except:
            print("Port not open on", portAddress, ":", port)





if __name__ == "__main__":
    def startClient(addr):
        print("Client is starting")
        clientNet = NetConnecter()
        clientNet.connectPort(addr)
        pass

    def startServer():
        print("Server is starting")
        serverNet = NetConnecter()
        threading.Thread(target=serverNet.openPort).start()
        
    def clientMessage():
        pass

    udpTest = NetConnecter()

    from tkinter import *
    root = Tk()
    root.title("Networking Test")
    root.geometry("500x100")
    cL = None
    f1 = Frame(root)
    e1 = Entry(f1, width=50, justify=CENTER)
    e1.insert(END, socket.gethostbyname(socket.gethostname()))
    e2 = Entry(f1, width=50, justify=CENTER)
    b1 = Button(f1, text="Start Client", command=lambda: startClient(e1.get()))
    b2 = Button(f1, text="Start 'Server'", command=startServer)
    b3 = Button(f1, text="Find open ports", command=lambda: udpTest.serverLister())
    b4 = Button(f1, text="UDP messaging", command=lambda: udpTest.broadcastServer())
    b5 = Button(f1, text="Stop finding ports", command=lambda: udpTest.leaveServerLister())
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