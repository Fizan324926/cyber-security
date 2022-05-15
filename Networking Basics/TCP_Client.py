# import socket library
import socket 

 # target host to for client and  # target port number 
SERVER_IP="www.google.com"
PORT=80
ADDR=(SERVER_IP,PORT)



 # creating client using socket
 # AF_INET used for ipv4 and SOCK_STREAM for TCP Protocol
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# connecting client with host
client.connect(ADDR) 

 # sending some data to host
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# receiving data from host and printing
resp=client.recv(4096) 
print(resp.decode()) 