import socket
from setting import Settings
from threading import Thread
import pickle
from time import sleep
#handles connections - spent way to long on this 
class Mysocket:
    def __init__(self) -> None:# had some problems with multithreading  
        self.recieved = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IsConnecting = False       
        self.connection = None
        self.lenofdata = 0
        self.CanDc = True
    def Host(data,wait = False): # starts hosting server

        def tothread(dataa:Mysocket):
            host = Settings.getValue('IpAddress')
            port = Settings.getValue('Port')
            dataa.server.bind((host, int(port))) 
            dataa.server.listen(1)
            c, addr = dataa.server.accept() 
            sleep(1)
            dataa.connection = c
            dataa.IsConnecting = True
            #dataa.sendData("Hello")
            dataa.startGetData()
            return c,addr
        if not wait:
            t = Thread(target=tothread,args=(data,))
            t.daemon = True
            t.start()
        else: 
            a = tothread(data)
            return a
    def Stop(data): # closes all connection
        data.IsConnecting = False
        data.server.close()
    def ConnectToHost(data): #connect to a host
        host = Settings.getValue('IpAddress')
        port = Settings.getValue('Port')
        try:
            data.server.connect((host, int(port)))
            sleep(1)
            data.IsConnecting = True
            data.startGetData()
        except:
            return False#if not connected return false 
        return True 
    def startGetData(data):
        def tothread(data):
            aconnection = data.connection or data.server
            try:
                while data.IsConnecting:
                    d = aconnection.recv(4096)
                    if d == b'': data.Stop(); break
                    if d:
                        data.recieved.insert(0,pickle.loads(d))
            except:# restart game or go to error screen if client disconnects 
                if data.CanDc:
                    from game import SocketDC
                    SocketDC()
        t = Thread(target=tothread,args=(data,))
        t.daemon = True
        t.start()
    def getAllData(self):
        return self.recieved
    def WaitForData(data):
        while len(data.recieved) <= data.lenofdata:
            a = 1 # yields the code until data is added 
        data.lenofdata +=1
        return data.recieved[0]#sends the first value 
    def sendData(data,obj):
        aconnection = data.connection or data.server
        aconnection.sendall(pickle.dumps(obj))
