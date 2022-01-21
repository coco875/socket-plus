from src import socket_plus
import traceback

headers_socket = [
    {
        "name": "id_type",
        "type": int,
        "len": 4
    }
]

format_socket = {
    0: [
        {
            "name": "len_msg",
            "type": int,
            "len": 12
        },
        {
            "name": "fl",
            "type": float,
            "len": "len_msg"
        }
    ]
}


def update(self):
    msg = "test message"
    self.add_to_send({"id_type": 0, "len_msg": 32, "fl": 0.6})
    msg = "c'est un test"
    self.add_to_send({"id_type": 0, "len_msg": 32, "fl": 0.9})
    msg = "bon ça marche iqimjdijqmoiejrfm"
    self.add_to_send({"id_type": 0, "len_msg": 100, "fl": 30})
    self.send()
    print(self.recv())


s = socket_plus.Server_connection(
    "localhost", 6000, headers_socket, format_socket, update=update)
s.start()
c = socket_plus.Client_connection(
    "localhost", 6000,  headers_socket, format_socket)

try:
    c.connect()
except TimeoutError:
    s.stop()
input()
try:
    print(c.recv())
except Exception as err:
    print(type(err))    # the exception instance
    print(err.args)     # arguments stored in .args
    print(err)
    s.stop()
    c.disconnect()
    input()
    print(traceback.format_exc())
else:
    c.add_to_send({"id_type": 0, "len_msg": 32, "fl": "4.05"})
    c.send()
    c.disconnect()
    s.stop()
