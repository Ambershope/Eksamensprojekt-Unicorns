import socket
import threading

def findPorts(port=35565):
    pass

class NetConecter():
    def __init__(self, port = 35565):
        self.port = port
        self.socket = socket.socket()

    def openPort(self):
        self.socket.bind(('', self.port))
        self.socket.listen()
        client, addr = self.socket.accept()
        print("Got connection from", addr)

    def connectPort(self, portAddress, port = 35565):
        try:
            self.socket.connect((portAddress, port))
        except:
            print("Port not open on", portAddress, ":", port)



if __name__ == "__main__":
    def startClient():
        print("Client is starting")
        clientNet = NetConecter()
        clientNet.connectPort("127.0.0.1")
        pass

    def startServer():
        print("Server is starting")
        serverNet = NetConecter()
        serverNet.openPort()
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