import socket

def findPorts(port="35565"):
    pass

class NetConecter():
    def __init__(self, port = "35565"):
        self.port = port
        self.socket = socket.socket()

    def openPort(self):
        self.socket.bind(('', self.port))

    def connectPort(self, portAddress, port):
        self.socket.connect((portAddress, port))



if __name__ == "__main__":
    print("Hello world")