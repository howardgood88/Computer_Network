from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
serverSocket.bind(('127.0.0.1', 8787))
serverSocket.listen(5)
while True:
	#Establish the connection
	print('Ready to serve...')
	connectionSocket, addr = serverSocket.accept()
	try:
		message = connectionSocket.recv(8192).decode()
		print('Request From Client %s %s: \n%s' % (addr, connectionSocket, message))
		filename = message.split(' ')[1]
		if filename == '/':
			filename = '/index.html'
		with open(filename[1:], 'r') as f:
			outputdata = f.read()
			#Send one HTTP header line into socket
		response = 'HTTP/1.1 200 OK\r\n\r\n'
		response += outputdata
		connectionSocket.send(response.encode())
		#connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n<html><body>hello</body></html>'.encode())

		#Send the content of the requested file to the client
		#for i in range(0, len(outputdata)):
		#	connectionSocket.send(outputdata[i].encode())
		#connectionSocket.send("\r\n".encode())
		connectionSocket.close()
	except:
		#Send response message for file not found
		response = 'HTTP/1.1 404 Not Found\r\n\r\n<html><body>\
		<div style="text-align:center;">\
			<div style="background-color:#FF1C1C; margin:0 auto;border: 2px solid blue; line-height:200px; font-size:30px;">HTTP/1.1 404 Not Found!</div>\
		</div>\
		</body</html>'
		connectionSocket.send(response.encode())
		#Close client socket
		connectionSocket.close()
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data 