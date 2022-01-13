import socket
import threading
from typing import Type

def normal_update(self):
    pass

def divided_list(liste:list, num:int) -> list[list]:
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
    num = 0
    pow_2 = 1
    for i in bit:
        num += pow_2*i
        pow_2 *= 2
    return int(num).to_bytes(1, "big")

def convert_bit(byt:bytes) -> list[int]:
    bit = []
    for i in byt:
        num_bit = bin(i)[2:]
        num_bit = "0"*(8-len(num_bit)) + num_bit
        num_bit = num_bit[::-1]
        for j in num_bit:
            bit.append(int(j))
    return bit

def convert_bytes(data:dict, bins:list, struct:dict) -> tuple[dict,list]:
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

class Client_connection:
    def __init__(self, adresse_ip:str, port:int, client_header:list[dict], client_format:list[dict], server_header:list[dict] = list[dict], server_format:list[dict] = list[dict]):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if server_header != list[dict]:
            self.s_header = server_header
        else:
            self.s_header = client_header
        
        if server_format != list[dict]:
            self.s_format = server_format
        else:
            self.s_format = client_format

        self.c_header = client_header
        self.c_format = client_format
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
        for i in self.c_header:
            self.list_bit += convert_to_bin(thing, i)
            last = thing[i["name"]]
        for i in self.c_format[last]:
            self.list_bit += convert_to_bin(thing, i)

    def send(self):
        bit_byte = divided_list(self.list_bit, 8)
        send = b""
        for i in bit_byte:
            send += convert_bit_byte(i)
        self.sock.send(send)

    def recv(self):
        msg = self.sock.recv(1024)
        bin_msg = convert_bit(msg)
        all_data = []
        while len(bin_msg) > 0:
            data = {}
            for i in self.s_header:
                d, bin_msg = convert_bytes(data, bin_msg, i)
                data.update(d)
            for i in self.s_format[data[list(data)[-1]]]:
                d, bin_msg = convert_bytes(data, bin_msg, i)
                data.update(d)
            all_data.append(data)
        return all_data

class Server_connection(threading.Thread):
    def __init__(self, adresse_ip: str, port: int, server_header: list[dict], server_format: list[dict], client_header: list[dict] = list[dict], client_format: list[dict] = list[dict], update:Type[normal_update] = normal_update):
        threading.Thread.__init__(self)
        if client_header != list[dict]:
            self.c_header = client_header
        else:
            self.c_header = server_header
        
        if client_format != list[dict]:
            self.c_format = client_format
        else:
            self.c_format = server_format

        self.s_header = server_header
        self.s_format = server_format
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
            else:
                clientsock.setblocking(1)
                newthread = ClientThread(client_adress, clientsock, self.s_header, self.s_format, self.c_header, self.c_format, self.update)
                newthread.start()
                self.all_thread.append(newthread)
    def stop(self) -> None:
        """stop server"""
        self.starting = False
        for i in self.all_thread:
            if i.is_alive():
                i.csocket.close()
        self.server.close()

class ClientThread(threading.Thread):
    def __init__(self, client_adress, clientsocket, server_header: list[dict], server_format: list[dict], client_header: list[dict], client_format: list[dict], update:Type[normal_update]):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.s_header = server_header
        self.s_format = server_format
        self.c_header = client_header
        self.c_format = client_format
        self.update = update
        print("New connection added: ", client_adress)
        self.client_adress = client_adress
        self.list_bit = []

    def run(self):
        print("Connection from : ", self.client_adress)
        self.update(self)

    def add_to_send(self, thing:dict) -> None:
        for i in self.s_header:
            self.list_bit += convert_to_bin(thing, i)
            last = thing[i["name"]]
        for i in self.s_format[last]:
            self.list_bit += convert_to_bin(thing, i)
    
    def send(self) -> None:
        bit_byte = divided_list(self.list_bit,8)
        send = b""
        for i in bit_byte:
            send += convert_bit_byte(i)
        self.csocket.send(send)
        print(send)
    
    def recv(self) -> list[dict]:
        msg = self.csocket.recv(1024)
        bin_msg = convert_bit(msg)
        all_data = []
        while len(bin_msg) > 0:
            data = {}
            for i in self.c_header:
                d, bin_msg = convert_bytes(data, bin_msg, i)
                data.update(d)
            for i in self.c_format[data[list(data)[-1]]]:
                d, bin_msg = convert_bytes(data, bin_msg, i)
                data.update(d)
            all_data.append(data)
        return all_data

def convert_to_bin(values:dict, struc:dict) -> list[list]:
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
        rep = []
        for i in ans:
            rep.append(int(i))
        rep.reverse()
        return rep
