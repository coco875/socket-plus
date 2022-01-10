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
    def __init__(self, adresse_ip: str, port: int, header: list, format_socket: list, update):
        threading.Thread.__init__(self)
        self.header = header
        self.format = format_socket
        self.update = update
        self.adresse_ip = adresse_ip
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.adresse_ip, port))
        self.starting = True
        self.all_thread = []
    def run(self):
        while self.starting:
            self.server.listen(1)
            try:
                clientsock, client_adress = self.server.accept()
            except OSError:
                pass
            except Exception as err:
                print(err)
            else:
                clientsock.setblocking(1)
                newthread = ClientThread(client_adress, clientsock, self.update, self.header, self.format)
                newthread.start()
                self.all_thread.append(newthread)
    def stop(self):
        """stop server"""
        self.starting = False
        for i in self.all_thread:
            if i.is_alive():
                i.csocket.close()
        self.server.close()

class ClientThread(threading.Thread):
    def __init__(self, client_adress, clientsocket, update, header:list, format_socket:dict):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.header = header
        self.format = format_socket
        self.update = update
        print("New connection added: ", client_adress)
        self.client_adress = client_adress
        self.list_bit = []

    def run(self):
        print("Connection from : ", self.client_adress)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        self.update(self)

    def add_to_send(self, thing:dict):
        for i in self.header:
            self.list_bit += convert_to_bin(thing, i)
            last = thing[i["name"]]
        for i in self.format[last]:
            self.list_bit += convert_to_bin(thing, i)
        print(self.list_bit)
    
    def send(self):
        divided_list(self.list_bit,8)

def convert_to_bin(values:dict, struc:dict) -> list:
    types = struc["type"]
    lenght = struc["len"]
    value = values[struc["name"]]
    if type(lenght) is str:
        lenght = values[lenght]
    print(lenght)
    ans = types(value)
    t = ""
    if types == int:
        ans = bin(ans)[2:]
        t += "0"*(lenght-len(ans))
        ans = t+ans
        rep = []
        for i in ans:
            rep.append(int(i))
        rep.reverse()
        return rep
    if types == str:
        ans = bytes(ans, 'utf-8')
        ans = int.from_bytes(ans, "big")
        ans = bin(ans)[2:]
        t += "0"*(lenght-len(ans))
        ans = t+ans
        rep = []
        for i in ans:
            rep.append(int(i))
        return rep

def divided_list(liste:list, num:int):
    list_div = []
    tmp = []
    for i in liste:
        tmp.append(i)
        if len(tmp) == num:
            list_div.append(tmp)
            tmp = []
    