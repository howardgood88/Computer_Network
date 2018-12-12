from socket import *
import base64
import ssl
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  # Added
from email.mime.image import MIMEImage

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.gmail.com' #Fill in start #Fill in end
# Create socket called clientSocket and establish a TCP connection with mailserver

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 587))
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
	print('220 reply not received from server.')
# Send HELO command and print server response.
heloCommand = 'EHLO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
	print('250 reply not received from server.')

clientSocket.send('starttls\r\n'.encode())
recv_tls = clientSocket.recv(1024)
print(recv_tls.decode())

clientSocket = ssl.wrap_socket(clientSocket, ssl_version = ssl.PROTOCOL_TLS)

#Info for username and password
print('Auth login...')
username = "howardgood88@gmail.com"
username = base64.b64encode(username.encode())
password = getpass.getpass('Enter password')
password = base64.b64encode(password.encode())
authMsg = "AUTH LOGIN\r\n"
clientSocket.send(authMsg.encode())
recv_auth = clientSocket.recv(1024)
print(recv_auth.decode())

clientSocket.send(username + b'\r\n')
#clientSocket.send("\r\n".encode())
recv_user = clientSocket.recv(1024)
print("Response after sending username: "+recv_user.decode())

end = b'\r\n'
#end = base64.b64encode(end.encode())
clientSocket.send(password + end)
#clientSocket.send("\r\n".encode())
recv_pass = clientSocket.recv(1024)
print("Response after sending password: "+recv_pass.decode())

# Send MAIL FROM command and print server response.
print('Send MAIL FROM command')
clientSocket.send('MAIL FROM:<105503008@cc.ncu.edu.tw>\r\n'.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '250':
	print('250 reply not received from server.')
# Send RCPT TO command and print server response.
print('Send RCPT TO command')
clientSocket.send('RCPT TO:<howardgood88@gmail.com>\r\n'.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '250':
	print('250 reply not received from server.')
# Send DATA command and print server response.
print('Send DATA command')
clientSocket.send('DATA\r\n'.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '354':
	print('354 reply not received from server.')
# Send message data.
print('Send message data')

msg = 'SUBJECT: SMTP Mail Client Test\nSMTP Mail Client Test\n'
#clientSocket.send(msg.encode())

# sending image
filepath = './python.jpg'

#msg = MIMEMultipart('related')
#msg["To"] = ''
#msg["From"] = ''
#msg["Subject"] = ''
mime = MIMEMultipart('')
text = MIMEText(msg)
mime.attach(text)
text = MIMEText('<img src="cid' + filepath + '">', 'html')
mime.attach(text)
with open(filepath, 'rb') as f:
	image = MIMEImage(f.read())
image.add_header('Content-ID', '<' + filepath + '>')
mime.attach(image)
msg = mime.as_string()
clientSocket.send(msg.encode())
'''
fp = open(attachment, 'rb')                                                    
img = MIMEImage(fp.read())
fp.close()
img.add_header('Content-ID', '<{}>'.format(attachment))
msg.attach(img)

print msg.as_string()
'''
clientSocket.send(b'\r\n.\r\n')
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '250':
	print('250 reply not received from server.')

# Send QUIT command and get server response.
print('Send QUIT command')
clientSocket.send('QUIT\r\n'.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '221':
	print('221 reply not received from server.')

print('Finished Mail')