# import socket library
import socket 

 # target host to for client and  # target port number 
target_host=socket.gethostbyname('www.google.com') 
target_port=80   


 # creating client using socket
 # AF_INET used for ipv4 and SOCK_STREAM for TCP Protocol
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# connecting client with host
client.connect((target_host,target_port)) 

 # sending some data to host
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# receiving data from host and printing
resp=client.recv(4096) 
print(resp.decode()) 