# importing libraries
from http import server
import socket 
import threading  

#   Declaring  variables

SERVER_IP=socket.gethostbyname(socket.gethostname())
PORT=9998
ADDR=(SERVER_IP,PORT)
HEADER=64
FORMAT='UTF-8'
DISCONNECT_MSG='!DISCONNECT'

# creating TCP server using socket

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

# function to start server and listing for clients

def start():
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER_IP}")
    while True:
        conn,addr=server.accept()  # get client connection
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


# function to handle clientvwhen it connects

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected!")
    connected=True
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length=int(msg_length)
            msg=conn.recv(msg_length).decode(FORMAT)
            if msg==DISCONNECT_MSG:
                connected=False
            print(f"[{addr}] {msg}")
            conn.send('MSG Received! '.decode(FORMAT))
    conn.close()



if __name__=='__main__':
    print(f'[STARTING] server is starting...')
    start()