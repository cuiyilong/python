import sys
import socket
import time
if len(sys.argv)!=3:
    print "input dst server!"
    sys.exit(0)

print sys.argv[1]

def udpclient(ip):
    addr = (ip,5678)


    udpsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    while True:
        msg = raw_input()
        if not msg:
            break
        udpsock.sendto(msg,addr)

    udpsock.close()
def tcpclient(ip):
    addr = (ip,8766)
    tcpsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcpsock.connect(addr)
    time.sleep(2)
    tcpsock.send('1')
    print tcpsock.recv(1024)
    tcpsock.close()


if(sys.argv[2] == 'udp'):
    udpclient(sys.argv[1])
elif (sys.argv[2] == 'tcp'):
    tcpclient(sys.argv[1])
else:
    print "invalid cient"
