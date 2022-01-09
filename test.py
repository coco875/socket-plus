import socket_game

s = socket_game.Server_connection(8000)
s.start()
c = socket_game.Client_connection("localhost", 8000)
input()
c.connect()
input()
s.stop()

