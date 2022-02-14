import threading
import socket_plus

client_header = [{"name": "id", "type": int, "len": 1}]

client_format = {
    0: [
        {"name": "len_psd", "type": int, "len": 7},
        {"name": "psd", "type": str, "len": "len_psd"},
    ],
    1: [
        {"name": "len_msg", "type": int, "len": 15},
        {"name": "msg", "type": str, "len": "len_msg"},
    ],
}

server_header = [{"name": "id", "type": int, "len": 1}]

server_format = {
    0: [
        {"name": "id_client", "type": int, "len": 7},
        {"name": "len_psd", "type": int, "len": 8},
        {"name": "psd", "type": str, "len": "len_psd"},
    ],
    1: [
        {"name": "id_client", "type": int, "len": 7},
        {"name": "len_msg", "type": int, "len": 16},
        {"name": "msg", "type": str, "len": "len_msg"},
    ],
}

client = socket_plus.Client_connection(
    "localhost", 6000, client_header, client_format, server_header, server_format
)

pseudo = input("pseudo: ")

client.add_to_send({"id": 0, "len_psd": len(bytes(pseudo, "utf-8")), "psd": pseudo})

client.send()

other_pseudo = {}

continues = True


class Client_tchat(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while continues:
            data = client.recv()
            if data["id"] == 0:
                other_pseudo[data["id_client"]] = data["psd"]
            else:
                print(other_pseudo[data["id_client"]] + ":", data["msg"])


while continues:
    message = input()
    client.add_to_send(
        {"id": 1, "len_msg": len(bytes(message, "utf-8")), "msg": message}
    )
    client.send()
