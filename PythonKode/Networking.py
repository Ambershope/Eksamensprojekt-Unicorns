import socket
import threading

def findPorts(port=35565):
    '''
    Finds a list of open ports on current internet
    \n*port is the port to search on. Deafault 35565.
    '''
    pass

class NetConecter():
    '''
    This class handels Networking in our game, \nHere we can open ports and connect to ports on certain addresses
    '''
    def __init__(self, port = 35565):
        self.port = port
        self.socket = socket.socket()
        self.stopServer = False
        self.client = None
        self.addr = None

    def openPort(self):
        '''
        This function should not be used with it self.
        \n.
        '''
        self.socket.bind(('', self.port))
        self.socket.listen()
        self.client, self.addr = self.socket.accept()
        print("Got connection from", self.addr)

    def connectPort(self, portAddress, port = 35565):
        '''
        This function should not be used on your own.
        \nInstead use connect().
        '''
        try:
            self.socket.connect((portAddress, port))
        except:
            print("Port not open on", portAddress, ":", port)



if __name__ == "__main__":
    def startClient():
        print("Client is starting")
        clientNet = NetConecter()
        clientNet.connectPort("10.160.219.215")
        pass

    def startServer():
        print("Server is starting")
        serverNet = NetConecter()
        threading.Thread(target=serverNet.openPort).start()
        pass

    from tkinter import *
    root = Tk()
    root.title("Networking Test")
    root.geometry("500x500")
    f1 = Frame(root)
    b1 = Button(f1, text="Start Client", command=startClient)
    b2 = Button(f1, text="Start 'Server'", command=startServer)
    t1 = Text(f1, height=25, width=50)
    l1 = Label(f1, text=" --- Netværks text --- ")
    f1.pack()
    l1.grid(row=0, column=0, columnspan=2)
    b1.grid(row=1, column=0)
    b2.grid(row=1, column=1)
    t1.grid(row=2, column=0, columnspan=2)
    root.mainloop()