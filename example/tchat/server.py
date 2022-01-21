import threading
import socket_plus

client_header = [
    {
        "name":"id",
        "type": int,
        "len": 1
    }
]

client_format = {
    0:[
        {
            "name":"len_psd",
            "type": int,
            "len": 7
        },
        {
            "name":"psd",
            "type": str,
            "len": "len_psd"
        }
    ],
    1:[
        {
            "name":"len_msg",
            "type": int,
            "len": 15
        },
        {
            "name":"msg",
            "type": str,
            'len': 'len_msg'
        }
    ]
}

server_header = [
    {
        "name":"id",
        "type": int,
        "len": 1
    }
]

server_format = {
    0:[
        {
            "name":"id_client",
            "type":int,
            "len":7
        },
        {
            "name":"len_psd",
            "type": int,
            "len": 8
        },
        {
            "name":"psd",
            "type": str,
            "len": "len_psd"
        }
    ],
    1:[
        {
            "name":"id_client",
            "type":int,
            "len":7
        },
        {
            "name":"len_msg",
            "type": int,
            "len": 16
        },
        {
            "name":"msg",
            "type": str,
            'len': 'len_msg'
        }
    ]
}

continues = True

tchat = []

class Server_tchat(threading.Thread):
    def __init__(self, id, client: socket_plus.Client_Thread):
        threading.Thread.__init__(self)
        self.client = client
        self.id = id
        self.tchat = tchat
    def run(self):
        while continues:
            if tchat != self.tchat:
                for i in range(len(self.tchat),tchat):
                    if tchat[i]["id"]!=self.id:
                        self.client.add_to_send({"id":1,"id_client":tchat[i]["id"]})

all_client = {}

all_thread:list[threading.Thread] = []

def update(self):
    data = self.recv()
    id = len(all_thread)
    client_thread = Server_tchat(id)
    all_client[id] = data["psd"]
    client_thread.start()
    all_thread.append(client_thread)

server = socket_plus.Server_connection('localhost', 6000, server_header, server_format, client_header, client_format)