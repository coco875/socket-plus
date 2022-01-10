import socket_game

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

s = socket_game.Server_connection("localhost", 8000, headers_socket, format_socket)
s.start()
c = socket_game.Client_connection("localhost", 8000,  headers_socket, format_socket)
c.connect()
input()
c.disconnect()
s.stop()
