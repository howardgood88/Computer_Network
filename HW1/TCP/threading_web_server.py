from socket import *
import sys # In order to terminate the program
import threading
import time

def client_treading(connectionSocket, addr, port, filename):
		print('Opening new port({}) to serve...'.format(port))
		serverSocket = socket(AF_INET, SOCK_STREAM)
		#Prepare a sever socket
		serverSocket.bind(('127.0.0.1', port))
		serverSocket.listen(1)
		head = 'HTTP/1.1 200 OK\r\n\r\n'
		new_url = '<HTML>\
<HEAD>\
	<meta charset="UTF-8">\
</HEAD>\
<BODY>\
	<div style="text-align:center;">\
		<div style="background-color:#7744FF; margin:0 auto;border: 2px solid blue; line-height:200px; font-size:30px;">\
			We will serve you at <a href="http://127.0.0.1:%d" target="_blank">http://127.0.0.1:%d</a> in port %d.\
			<br>Please go to take a look!</div>\
	</div>\
</BODY>\
</HTML>' % (port, port, port)
		message = head + new_url
		connectionSocket.send(message.encode())
		connectionSocket.close()
		while True:
			try:
				serverSocket.settimeout(10)
				connectionSocket, addr = serverSocket.accept()
				message = connectionSocket.recv(8192).decode()
				print('New Request to new port recieved!')
				filename = message.split(' ')[1]
				if filename == '/':
					filename = '/index.html'
				with open(filename[1:], 'r') as f:
					outputdata = f.read()
				relocate = 'HTTP/1.1 200 OK\r\n\r\n'
				relocate += outputdata
				connectionSocket.send(relocate.encode())
				connectionSocket.close()
			except timeout:
				print('Disconnecting from port {} server!'.format(port))
				serverSocket.close()
				break
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

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
serverSocket.bind(('127.0.0.1', 8787))
serverSocket.listen(1)
Threads = []
port = 8787
while True:
	#Establish the connection
	print('Ready to serve...')
	connectionSocket, addr = serverSocket.accept()
	message = connectionSocket.recv(8192).decode()
	if not message:
		continue
	filename = message.split(' ')[1]
	if filename == '/':
		filename = '/index.html'
	elif filename == '/favicon.ico':
		continue
	print('Request to main port recieved!')
	port += 1
	Threads.append(threading.Thread(target=client_treading, args=(connectionSocket, addr, port, filename)).start())
	time.sleep(0.5)

for element in Threads:
	element.join()
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data