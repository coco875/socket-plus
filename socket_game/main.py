import socket
import threading

class Client_connection:
    def __init__(self, ip:str, port:int, header:list, format:list):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.header = header
        self.format = format
        #self.sock.settimeout(0)
        self.ip = ip
        self.port = port
    
    def disconnect(self):
        self.sock.close()
    
    def connect(self):
        self.sock.connect((self.ip, self.port))

class Server_connection(threading.Thread):
    def __init__(self, port: int, header: list, format: list):
        threading.Thread.__init__(self)
        self.header = header
        self.format = format
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("localhost", port))
    def run(self):
        self.go = True
        self.all_thread = []
        while self.go:
            self.server.listen(1)
            clientsock, clientAddress = self.server.accept()
            clientsock.setblocking(1)
            newthread = ClientThread(clientAddress, clientsock)
            newthread.start()
            self.all_thread.append(newthread)
    def stop(self):
        self.go = False
        for i in self.all_thread:
            i.csocket.close()
        self.server.close()

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("New connection added: ", clientAddress)
        self.clientAddress = clientAddress

    def run(self):
        print("Connection from : ", self.clientAddress)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg == 'bye':
              break
            print("from client", msg)
            self.csocket.send(bytes(msg, 'UTF-8'))
        print("Client at ", clientAddress, " disconnected...")
