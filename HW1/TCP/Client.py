from socket import *
import sys


serverName = sys.argv[1]
serverPort = sys.argv[2]
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, int(serverPort)))
message = 'GET %s HTTP/1.1\r\n\
Host: %s:%s\
Connection: keep-alive\
Cache-Control: max-age=0\
Upgrade-Insecure-Requests: 1\
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\
Accept-Encoding: gzip, deflate, br\
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6\
' % (sys.argv[3], serverName, serverPort)
print(message)
clientSocket.send(message.encode())
receive_message = clientSocket.recv(8192)
print('Server Reply:', receive_message.decode())
clientSocket.close( )