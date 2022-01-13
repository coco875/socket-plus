import socket_plus

headers_socket = [
    {
        "name":"id_type",
        "type":int,
        "len":4
    }
]

format_socket = {
    0:[
        {
            "name":"len_msg",
            "type":int,
            "len":4
        },
        {
            "name":"msg",
            "type":str,
            "len":"len_msg"
        }
    ]
}

def update(self):
    self.add_to_send({"id_type": 0, "len_msg": 4, "msg": "bite"})
    self.send()
    self.recv()
    # msg = ''
    # while True:
    #     data = self.csocket.recv(2048)
    #     msg = data.decode()
    #     if msg == 'bye':
    #         break
    #     print("from client", msg)
    #     self.csocket.send(bytes(msg, 'UTF-8'))
    # print("Client at ", self.client_adress, " disconnected...")
    
s = socket_plus.Server_connection("localhost", 6000, headers_socket, format_socket, update=update)
s.start()
c = socket_plus.Client_connection(
    "localhost", 6000,  headers_socket, format_socket)
try:
    c.connect()
except TimeoutError:
    s.stop()
input()
c.recv()
c.add_to_send({"id_type": 0, "len_msg": 4, "msg": " oi"})
c.send()
input()
c.disconnect()
s.stop()
