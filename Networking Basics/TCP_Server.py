# importing libraries
import socket 
import threading  

IP='0.0.0.0'
port=9998

def main():
    # creating TCP server using socket 
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # bind server to start listening for maximum of 5 back log connections
    server.bind((IP,port))
    server.listen(5)
    print(f'Listening on {IP}:{port}')

    while True:
        # when client connects we get both its address and client info
        client,addr=server.accept()
        print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')

        # creating thread for client with client handler function
        client_handler=threading.Thread(target=handle_client,args=(client,))
        client_handler.start()

# function to handle client when it connects
def handle_client(client_sock):
    with client_sock as sock:
        request=sock.recv(4096)
        print(f'[*] Received: {request.decode("utf-8")}')
        request.send('ACK')
if __name__=='__main__':
    main()