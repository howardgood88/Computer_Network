# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import random
from socket import *
from time import time, sleep
import sys
import threading

listen_flag = True
heartbeat_flag = True

server_ip = '127.0.0.1'
server_port = 8787
# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind((server_ip, server_port))
i = 1
while True:
	def send_heartbeat(serverSocket, address, message):
		try:
			while True:
				global i
				message = 'heartbeat {} {}'.format(i, time())
				serverSocket.sendto(message.encode(), address)
				i += 1
				sleep(5)
		except:
			serverSocket.close()
			sys.exit()

	# Generate random number in the range of 0 to 10
	rand = random.randint(0, 10)
	# Receive the client packet along with the address it is coming from
	message, address = serverSocket.recvfrom(1024)
	# Capitalize the message from the client
	message_origen = message.decode().upper()
	# If rand is less is than 4, we consider the packet lost and do not respond
	message = message_origen.split(' ')
	if message[0] != 'PING' and message[0] != 'HEARTBEAT':
		seq_num = message[0]
		loss_num = message[1]
		print('Heartbeat package({}) lost: {}'.format(seq_num, loss_num))
		if float(loss_num) > 1.0:
			print('Disconnect from server...')
			clientSocket.close()
			sys.exit()
	if rand < 3:
		continue

	if message[0] == 'HEARTBEAT':
		if heartbeat_flag:
			threading.Thread(target=send_heartbeat, args=(serverSocket, address, message)).start()
			heartbeat_flag = False

		num = message[1]
		timestamp = message[2]

		if listen_flag:
			temp = timestamp
			listen_flag = False

		current_time = time()
		if float(timestamp) - float(temp) > 7:
			timestamp = temp
			temp = current_time
		else:
			temp = timestamp
		time_difference = current_time - float(timestamp)
		loss_num = int(time_difference / 5)
		if loss_num != 0:
			loss_num -= 1
		serverSocket.sendto((str(num) + ' ' + str(loss_num)).encode(), address)
		if loss_num > 1:
			print('Client application has stopped!')
			break

	elif message[0] == 'PING':
		# Otherwise, the server responds
		serverSocket.sendto(message_origen.encode(), address)

serverSocket.close()
sys.exit()