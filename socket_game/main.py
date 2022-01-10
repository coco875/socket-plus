import socket
import threading

class Client_connection:
    def __init__(self, adresse_ip:str, port:int, header:list, format_socket:list):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.header = header
        self.format = format_socket
        #self.sock.settimeout(0)
        self.adresse_ip = adresse_ip
        self.port = port

    def disconnect(self):
        """disconnect client from server"""
        self.sock.close()

    def connect(self):
        """connect client from server"""
        self.sock.connect((self.adresse_ip, self.port))

class Server_connection(threading.Thread):
    def __init__(self, adresse_ip: str, port: int, header: list, format_socket: list):
        threading.Thread.__init__(self)
        self.header = header
        self.format = format_socket
        self.adresse_ip = adresse_ip
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.adresse_ip, port))
        self.starting = True
        self.all_thread = []
    def run(self):
        while self.starting:
            self.server.listen(1)
            clientsock, client_adress = self.server.accept()
            clientsock.setblocking(1)
            newthread = ClientThread(client_adress, clientsock)
            newthread.start()
            self.all_thread.append(newthread)
    def stop(self):
        """stop server"""
        self.starting = False
        for i in self.all_thread:
            i.csocket.close()
        self.server.close()

class ClientThread(threading.Thread):
    def __init__(self, client_adress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("New connection added: ", client_adress)
        self.client_adress = client_adress

    def run(self):
        print("Connection from : ", self.client_adress)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg == 'bye':
                break
            print("from client", msg)
            self.csocket.send(bytes(msg, 'UTF-8'))
        print("Client at ", client_adress, " disconnected...")
