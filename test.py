import time
import json
import socket
host = '127.0.0.1'
port =1309
udpSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Send
#udpSocket.sendto("Testing ".encode('utf-8'),(host,port))
#

#recieve
UDPSock.bind((host,port))
while(True):
    data,addr = UDPSock.recvfrom(buffer)
    if len(data)>0:
        print(data)
    time.sleep(0.0001)
#


UDPSock.close()
