from socket import *
import sys
if len(sys.argv) <= 0:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
tcpSerSock.bind(('127.0.0.1',8008))
tcpSerSock.listen(5)
# Fill in end.
while True:
    # Strat receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024).decode()# Fill in start. # Fill in end.
    print(message)
    # Extract the filename from the given message
    print(message.split()[1])
    if message.split()[0].upper() == 'POST':
        website = str(message.split()[-1])
        for i in range(len(website)):
            if website[i] == '=':
                filename = website[i+1:]
                break
    else:
        filename = message.split()[1].partition("/")[2]
    #filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:# Check wether the file exist in the cache
        f = open(filetouse[1:], "r", encoding = 'utf-8')
        outputdata = f.read()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.1 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n".encode())
        # Fill in start.
        tcpCliSock.send(outputdata.encode())
        # Fill in end.
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            # Fill in start. # Fill in end.
            hostn = filename.replace("www.","",1)
            print(hostn)
            try:
                # Connect to the socket to port 80
                # Fill in start.
                c.connect((hostn, 80))
                # Fill in end.
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                # fileobj = c.makefile('rwb', 0)
                # f.write(("GET "+"http://" + filename + "HTTP/1.0\n\n").encode())
                # Read the response into buffer
                buff = "GET " + '/ ' + "HTTP/1.1\r\n\r\n"
                # Fill in start.# Fill in end.
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                # Fill in start.
                c.send(buff.encode())
                content = c.recv(200000)
                tcpCliSock.send(content)
                tmpFile = open("./" + filename,"wb")
                tmpFile.write(content)
                fileobj.close()
                tmpFile.close()
                # Fill in end.
            except:
                print("Illegal request")
                tcpCliSock.send('HTTP/1.1 404 Not Found \r\n\r\n'.encode())
        else:
            # HTTP response message for file not found
            # Fill in start.
            tcpCliSock.send("HTTP/1.1 404 Not Found \r\n\r\n".encode())
            # Fill in end.
            # Close the client and the server sockets
            tcpCliSock.close()
    # Fill in start.
    # Fill in end.
