
# socket-plus

A library in python to communicate as efficiently as possible with structures.
to install:  
`pip install socket-plus`  
You can have some bugs and is not finished yet but it works.

# How to use

you need a list of dictionaries with how is formatted the header of data. Like this:  

```py
headers_socket = [
    {
        "name":"id_type",
        "type":int,
        "len":4
    }
]
```  

with this example is mean the first element of the headers have a name like "id_type", the type is int and take 4 bit.
All int is mesured by bit, this means this int can go to 0 at 2<sup>4</sup>-1 equal 15 if the given number is over you will get a error on the server or the client.

for the body when you have the main data it is also a list of dict. Like this:  

```py
format_socket = {
    0:[
        {
            "name":"len_msg",
            "type":int,
            "len":12
        },
        {
            "name":"msg",
            "type":str,
            "len":"len_msg"
        }
    ]
}
```

This means when the header is 0 this format is applied for the rest.
We have the first element which is an int with name "len_msg" (you can use space) with a len of 12 bit (0 at 2<sup>12</sup>-1 that is 4 095). The second element has a name like "msg" with type str and len "len_msg". With str the len is in byte. One letter is not necessarily one byte for exemple "ç" is two bytes. for len, it is not a number, it is a str, by doing this, this means that it takes the value in data, which means the len of msg is equal to the number of len_msg.  

to setup the client, it is this line:

```py
client = socket_plus.Client_connection("localhost", 6000,  headers_socket, format_socket)
```

to setup the server, it is this line:

```py
server = socket_plus.Server_connection("localhost", 6000, headers_socket, format_socket, update=update)
```

In first is ip "localhost", it is if you are in the same machine, else it is a str like this: "540.804.530.782". The second argument is the port as an int. The third and four arguments are for headers and the format that you defined before. update is a function to use when a client connect (this means more than one client can connect to the server, server is a multithread this means you need to call server.start to start). For example:

```py
def update(self):
    msg = "test message"
    self.add_to_send({"id_type": 0, "len_msg": len(msg), "msg": msg}) # add to send more details after
    msg = "it's work"
    self.add_to_send({"id_type": 0, "len_msg": len(msg), "msg": msg})
    self.send() # send all info
    print(self.recv()) # print what you receive from client
```

Inside this example we have some functions. self.add_to_send to add data while respecting the header that you gave before, and for the format it is the same. This means you send an id_type 0 with len_msg equal to the len of msg and with msg equal to msg that you have defined before. for client it is client.add_to_send also. self.send() to send all data you entered before, same for client. and self.recv to receive from client, for client it is the same but you receive from the server.

# More about

The main server is a thread, and other connections generates new threads so if you want to stop, you need to call server.stop(). So it generates a "bug" if the main thread (the place where the main code is executed) crash, other thread will continue to run so you need to force to quit with task manager or other.

when you init you can give other arguments if you have two protocols, one for the server and the other for the client. Like this :

```py
socket_plus.Client_connection("localhost", 6000, client_header=c_headers, client_format=c_formats, server_header=s_headers, server_format= s_format)
```

For client and servers, it is :

```py
socket_plus.Server_connection("localhost", 6000, server_header=s_headers, server_format=s_formats, client_header=c_headers, client_format=c_format, update=update)
```

when s_headers is header of server it is how server send data and s_formats is same but it is for the format c_headers, it is the same for clients and also for c_format. If you have a suggestion it is [here](https://github.com/coco875/socket-plus/issues). If you have a question we can talk [here](https://github.com/coco875/socket-plus/discussions/categories/q-a).
