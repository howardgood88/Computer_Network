from socket import *
import sys

if len(sys.argv) <= 0:
	print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
	sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
#print(sys.argv[1])
tcpSerSock.bind(('127.0.0.1', 8888))
tcpSerSock.listen(5)

while 1:
	# Strat receiving data from the client
	#print('Ready to serve...')
	tcpCliSock, addr = tcpSerSock.accept()
	#print('Received a connection from:', addr)
	message = tcpCliSock.recv(1024).decode()
	try:
		path = message.split()[1]
	except IndexError:
		print('list out od range error')
	if path == '/favicon.ico':
		continue
	elif path[:7] == '/images':
		continue
	elif path[:7] == '/client':
		continue
	elif path[:7] == '/xjs/_/':
		continue
	#print(message)
	# Extract the filename from the given message
	try:
		if message.split()[0] == 'POST' or message.split()[0] == 'post':
			print(message.split()[0])
			url = str(message.split()[-1])
			for i in range(len(url)):
				if url[i] == '=':
					filename = url[i + 1:]
					break
		else:
			print(path)
			filename = path.partition("/")[2]
	except IndexError:
		print('list out od range error')
	fileExist = "false"
	filetouse = "/" + filename
	try:
		# Check wether the file exist in the cache
		f = open(filetouse[1:], "r")
		print('Catch a cached file!')
		outputdata = f.read()
		fileExist = "true"
		# ProxyServer finds a cache hit and generates a response message
		tcpCliSock.send("HTTP/1.1 200 OK\r\n".encode())
		tcpCliSock.send("Content-Type:text/html\r\n".encode())
		tcpCliSock.send(outputdata.encode())
		f.close()
		print('Read from cache!')
	# Error handling for file not found in cache
	except IOError:
		if fileExist == "false":
			print('Cannot find cached file')
			# Create a socket on the proxyserver
			c = socket(AF_INET, SOCK_STREAM)
			#hostn = filename.replace("www.","",1)
			# Connect to the socket to port 80
			print('Conneting to %s...' % filename)
			try:
				c.connect((filename, 80))
				print('Connected!')
				# Create a temporary file on this socket and ask port 80 for the file requested by the client
				#fileobj = c.makefile('wrb', 100)
				#print('2')
				#fileobj.write(b"GET "+b"http://" + filename.encode() + b" HTTP/1.1\n\n")
				# Read the response into buffer
				buff = "GET " + '/ ' + "HTTP/1.1\r\n\r\n"
				# Create a new file in the cache for the requested file. Also send the response in the buffer to client socket and the corresponding file in the cache
				#print('1')
				#tmpFile.write(buff.encode())
				c.send(buff.encode())
				print('Sending request to %s...' % filetouse)
				recv_msg = c.recv(150000)
				print('Received reponse from %s' % filetouse)
				print('Opening new cache file...')
				tmpFile = open("./" + filename,"wb")
				print('Saving response to cache file...')
				tmpFile.write(recv_msg)
				print('Saved!')
				tcpCliSock.send(recv_msg)
				print('Sending response to browser...')
				print('Done!')
			except:
				print("Illegal request")
				tcpCliSock.send("HTTP/1.1 404 sendErrorErrorError\r\n".encode())
				tcpCliSock.send("Content-Type:text/html\r\n".encode())
				tcpCliSock.send("\r\n".encode())
		else:
			# HTTP response message for file not found
			tcpCliSock.send("HTTP/1.1 404 sendErrorErrorError\r\n".encode())
			tcpCliSock.send("Content-Type:text/html\r\n".encode())
			tcpCliSock.send("\r\n".encode())
	# Close the client and the server sockets
	print()
	tcpCliSock.close()
tcpSerSock.close()