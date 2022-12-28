import socket
import threading
PORT= 60000
HOST = socket.gethostbyname(socket.gethostname())
ADDRESS=(HOST,PORT)
FORMAT="utf-8"
clients,names=[],[]
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDRESS)
def startchat():
    print("Server is working on"+ HOST)
    server.listen()
    while True:
        connection,address= server.accept()
        connection.send("NAME".encode(FORMAT))

        name=connection.recv(1027).decode(FORMAT)

        names.append(name)
        clients.append(connection)
        print(f"Name is:{name}")
        broadcastmessage(f"{name} has joined the group".encode(FORMAT))
        connection.send("Connection successful",encode(FORMAT))
        thread=threading.Thread(target=receive,args=(connection,address))
        thread.start()
        print(f"active connections {threading.active_count()-1}")
def receive(connection,address):
    print(f"New connection {address}")
    connected=True
    while connected:
        message=connection.recv(1027)
        broadcastmessage(message)
    connection.close()
def broadcastmessage(message):
    for client in clients:
        client.send(message)
startchat()