import socket
import threading
from typing import List, Tuple

class Client_connection:
    def __init__(self, adresse_ip:str, port:int, header:list, format_socket:list):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.header = header
        self.format = format_socket
        #self.sock.settimeout(0)
        self.adresse_ip = adresse_ip
        self.port = port
        self.list_bit = []

    def disconnect(self):
        """disconnect client from server"""
        self.sock.close()

    def connect(self):
        """connect client from server"""
        self.sock.connect((self.adresse_ip, self.port))
    
    def add_to_send(self, thing: dict):
        for i in self.header:
            self.list_bit += convert_to_bin(thing, i)
            last = thing[i["name"]]
        for i in self.format[last]:
            self.list_bit += convert_to_bin(thing, i)

    def send(self):
        bit_byte = divided_list(self.list_bit, 8)
        send = b""
        for i in bit_byte:
            send += convert_bit_byte(i)
        self.sock.send(send)
        print(send)

    def recv(self):
        msg = self.sock.recv(1024)
        bin_msg = convert_bit(msg)
        data = {}
        while len(bin_msg)>0:
            for i in self.header:
                d, bin_msg = convert_bytes(data, bin_msg, i)
                data.update(d)
            for i in self.format[data[list(data)[-1]]]:
                d, bin_msg = convert_bytes(data, bin_msg, i)
                data.update(d)
        print(data)

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
    
    def send(self):
        bit_byte = divided_list(self.list_bit,8)
        send = b""
        for i in bit_byte:
            send += convert_bit_byte(i)
        self.csocket.send(send)
        print(send)
    
    def recv(self):
        msg = self.csocket.recv(1024)
        bin_msg = convert_bit(msg)
        data = {}
        while len(bin_msg) > 0:
            for i in self.header:
                d, bin_msg = convert_bytes(data, bin_msg, i)
                data.update(d)
            for i in self.format[data[list(data)[-1]]]:
                d, bin_msg = convert_bytes(data, bin_msg, i)
                data.update(d)
        print(data)

def convert_to_bin(values:dict, struc:dict) -> List[list]:
    types = struc["type"]
    lenght = struc["len"]
    value = values[struc["name"]]
    if type(lenght) is str:
        lenght = values[lenght]
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
        ans += " "*(lenght-len(ans))
        ans = bytes(ans, 'utf-8')
        ans = int.from_bytes(ans, "big")
        ans = bin(ans)[2:]
        t += "0"*((lenght*8)-len(ans))
        ans = ans
        print(ans)
        rep = []
        for i in ans:
            rep.append(int(i))
        rep.reverse()
        return rep

def divided_list(liste:list, num:int) -> List[list]:
    list_div = []
    tmp = []
    for i in liste:
        tmp.append(i)
        if len(tmp) == num:
            list_div.append(tmp)
            tmp = []
    list_div.append(tmp)
    return list_div

def convert_bit_byte(bit:list) -> bytes:
    #bit.reverse()
    num = 0
    pow_2 = 1
    for i in bit:
        num += pow_2*i
        pow_2 *= 2
    return int(num).to_bytes(1, "big")

def convert_bit(byt:bytes) -> List[int]:
    bit = []
    for i in byt:
        num_bit = bin(i)[2:]
        num_bit = "0"*(8-len(num_bit)) + num_bit
        num_bit = num_bit[::-1]
        for j in num_bit:
            bit.append(int(j))
    return bit

def convert_bytes(data:dict, bins:list, struct:dict) -> Tuple[dict,list]:
    lenght = struct["len"]
    if type(lenght) is str:
        lenght = data[lenght]
    traited_bin = bins[:lenght]
    if struct["type"]==int:
        tmp_num = 1
        num = 0
        for i in traited_bin:
            num += tmp_num*i
            tmp_num *= 2
        return {struct["name"]:num}, bins[lenght:]
    if struct["type"]==str:
        lenght *= 8
        traited_bin = bins[:lenght]
        tmp_num = 1
        num = 0
        for i in traited_bin:
            num += tmp_num*i
            tmp_num *= 2
        chn = int.to_bytes(num, int(lenght/8), "big")
        return {struct["name"]: chn.decode('utf-8')}, bins[lenght:]
