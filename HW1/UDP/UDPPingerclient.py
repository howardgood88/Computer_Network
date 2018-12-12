from socket import *
import time
from datetime import datetime, timedelta
import sys
import threading

server_ip = '127.0.0.1'
server_port = 8787
clientSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
# Generate random number in the range of 0 to 10
# Receive the client packet along with the address it is coming from

recieved = 0
RTT_list = []
print('Ping {}:'.format(server_ip))
for num in range(10):
	try:
		start_time = time.time()
		message = 'Ping {} {}'.format(num + 1, start_time)
		clientSocket.sendto(message.encode(), (server_ip, server_port))
		clientSocket.settimeout(2)

		message, address = clientSocket.recvfrom(1024)
		RTT = time.time() - start_time
		print('Reply from {}: {}, RTT: {:0.15f}s'.format(address, message.decode(), RTT))
		RTT_list.append(float(RTT))
		recieved += 1

	except timeout:
		# If rand is less is than 4, we consider the packet lost and do not respond
		# Otherwise, the server responds
		print('Request timed out...')

print()
print('The statistic of pinging {}:'.format(server_ip))
print('	Packet: Sended = {}, Recieved = {}, Lossed = {} ({}% loss)'.format(num + 1, recieved,
	num + 1 - recieved, (num + 1 - recieved) / (num + 1) * 100))
print('RTT(s):')
print(' 	Minimum = {:0.15f}s, Maximum = {:0.15f}s, Average = {:0.15f}s'.format(min(RTT_list), max(RTT_list), sum(RTT_list) / (num + 1)))

clientSocket.settimeout(None)
print()
print('Heartbeat service is on!')
i = 1
listen_flag = True
def recieve(clientSocket, message):
	global listen_flag
	while True:
		message, address = clientSocket.recvfrom(1024)
		message = message.decode().split(' ')
		if message[0] == 'heartbeat':
			num = message[1]
			timestamp = message[2]

			if listen_flag:
				temp = timestamp
				listen_flag = False

			current_time = time.time()
			if float(timestamp) - float(temp) > 7:
				print('I will never loss')
				timestamp = temp
				temp = current_time
			else:
				temp = timestamp
			time_difference = current_time - float(timestamp)
			loss_num = int(time_difference / 5)
			if loss_num != 0:
				loss_num -= 1
			clientSocket.sendto((str(num) + ' ' + str(loss_num)).encode(), address)
			if loss_num > 1:
				print('Client application has stopped!')
				break
		else:
			seq_num = message[0]
			loss_num = message[1]
			print('Heartbeat package({}) lost: {}'.format(seq_num, loss_num))
			if float(loss_num) > 1.0:
				print('Disconnect from server...')
				clientSocket.close()
				sys.exit()
threading.Thread(target=recieve, args=(clientSocket, message)).start()
try:
	while True:
		message = 'heartbeat {} {}'.format(i, time.time())
		clientSocket.sendto(message.encode(), address)
		i += 1
		time.sleep(5)
except:
	clientSocket.close()
	sys.exit()