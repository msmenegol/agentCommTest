import socket
import os
import sys
import time
import select
import re
import math


#SERVER
####constants####
BOBPORT = 6969
ALICEPORT = 6970

####methods####
def decodeSock(msg, port):
    return msg[:-1]

def encodeSock(msg, port):
    return msg + '\n'

def createSocket(TCP_PORT):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(('localhost', TCP_PORT))
    serverSocket.listen(5)

    return serverSocket

def sendTo(port, sList, msg): #sendTo(port socket to send, list of sockets, message)
    for s in sList:
        if port in s.getsockname():
            s.sendall(encodeSock(msg,port))

####variable initialization####
localPorts = [BOBPORT, ALICEPORT]
sockList = [] #sockets accepted
lastTime = time.time()

#Connect to all sub-systems (sockets) before anything
for p in localPorts:
    sock = createSocket(p)
    clientSock, address = sock.accept()
    sockList.append(clientSock)

while True:
    #Check which sockets are readable or writable
    readable, writable, exceptional = select.select(sockList, sockList, sockList, 0.1)

    #Interpret received messages
    for s in readable: #for every socket object
        _, receivePort = s.getsockname(); #receivePort = port_number

        data = s.recv(1024)
        if data != '': #if it's not a null message
            decodeData = decodeSock(data, receivePort)

            if '*' in decodeData:
                if receivePort == ALICEPORT:
                    sendTo(BOBPORT,writable,encodeSock(decodeData,BOBPORT))
                    print('sending msg to bob')
                    print(decodeData)
                if receivePort == BOBPORT:
                    sendTo(ALICEPORT,writable,encodeSock(decodeData,ALICEPORT))
                    print('sending msg to alice')
                    print(decodeData)
            else:
                print("un-message: " + decodeData)

    time.sleep(0.02)
#copter.close()
