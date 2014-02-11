import sys
import socket

addr = ('127.0.0.1',8766)
tcpsock = socket.socket(socket.AF_INET
                        ,socket.SOCK_STREAM
                        )


tcpsock.bind(addr)
tcpsock.listen(5)
while True:
    connect,addr = tcpsock.accept()
    buf = connect.recv(1024)
    if(buf == '1'):
         connect.send('welcome to server')
    else:
         connect.send('go out')
    connect.close()
tcpsock.close()
    
