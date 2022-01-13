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
    msg = "test message"
    self.add_to_send({"id_type": 0, "len_msg": len(msg), "msg": msg})
    msg = "c'est un test"
    self.add_to_send({"id_type": 0, "len_msg": len(msg), "msg": msg})
    msg = "alors ça marche plusieur"
    self.add_to_send({"id_type": 0, "len_msg": len(msg), "msg": msg})
    self.send()
    print(self.recv())
    
s = socket_plus.Server_connection("localhost", 6000, headers_socket, format_socket, update=update)
s.start()
c = socket_plus.Client_connection(
    "localhost", 6000,  headers_socket, format_socket)
try:
    c.connect()
except TimeoutError:
    s.stop()
print(c.recv())
c.add_to_send({"id_type": 0, "len_msg": 4, "msg": " oi"})
c.send()
c.disconnect()
s.stop()
