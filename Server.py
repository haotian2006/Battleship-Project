from RemoteHandler import Mysocket #testing with server 
import socket
import time
s = socket.socket()
s.connect(('localhost',25565))
while True:
    1+1