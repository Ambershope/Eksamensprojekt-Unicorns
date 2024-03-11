import socket
import threading

def findPorts(port=35565):
    '''
    Finds a list of open ports on current internet
    \n*port is the port to search on. Default 35565.
    '''
    pass

class NetConnecter():
    '''
    This class handels Networking in our game, \nHere we can open ports and connect to ports on certain addresses
    '''
    def __init__(self, port = 35565):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stopServer = False
        self.client = None
        self.addr = None

    def openPort(self):
        '''
        This function should not be used with it self.
        \n.
        '''
        addr = (socket.gethostbyname(socket.gethostname()), self.port)
        self.socket.bind(addr)
        print("Server open on", addr[0], ":", addr[1])
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
    def startClient(addr):
        print("Client is starting")
        clientNet = NetConnecter()
        clientNet.connectPort(addr)
        pass

    def startServer():
        print("Server is starting")
        serverNet = NetConnecter()
        threading.Thread(target=serverNet.openPort).start()
        pass

    from tkinter import *
    root = Tk()
    root.title("Networking Test")
    root.geometry("500x500")
    f1 = Frame(root)
    e1 = Entry(f1, width=50, justify=CENTER)
    e1.insert(END, '127.0.0.1')
    b1 = Button(f1, text="Start Client", command=lambda: startClient(e1.get()))
    b2 = Button(f1, text="Start 'Server'", command=startServer)
    t1 = Text(f1, height=20, width=50)
    l1 = Label(f1, text=" --- Netværks text --- ")
    f1.pack()
    l1.grid(row=0, column=0, columnspan=2)
    b1.grid(row=1, column=0)
    b2.grid(row=1, column=1)
    e1.grid(row=2, column=0, columnspan=2, )
    t1.grid(row=3, column=0, columnspan=2)
    root.mainloop()