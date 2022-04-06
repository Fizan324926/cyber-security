# import socket 
import socket

# seeting target host and port
target_host='www.google.com'
target_port=9997

# creating a UDP client
# AF_INET is used for IPv4 
# DGRAM is used for UDP Client 
client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)   

# sending data to host 
# UDP don't need connection first

client.sendto(b"SAMPLE",(target_host,target_port))

# receiving data from host
data,addr=client.recvfrom(4096)

# print response
print(data.decode())