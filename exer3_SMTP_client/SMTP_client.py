from socket import *

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
# Choose a mail server (e.g. Google mail server) and call it mailserver

###
# unsafe or unauthenticated connection is refused by most SMTP server
###

mailserver = ("smtp.elasticemail.com", 25)
# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')
# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
mailFromCommand = 'MAIL FROM:<wanderingxs@gmail.com>\r\n'
clientSocket.send(mailFromCommand.encode())
recv2 = clientSocket.recv(1024).decode()
print("Response after MAIL FROM command:", recv2)
if recv2[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
rcptToCommand = 'RCPT TO:<22415056@zju.edu.cn>\r\n'  # Fill with recipient email
clientSocket.send(rcptToCommand.encode())
recv3 = clientSocket.recv(1024).decode()
print("Response after RCPT TO command:", recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
recv4 = clientSocket.recv(1024).decode()
print("Response after DATA command:", recv4)
if recv4[:3] != '354':
    print('354 reply not received from server.')

# Send message data.
message = 'Subject: SMTP test mail\r\n\r\nThis is a test email sent using SMTP protocol.\r\n'
clientSocket.send(message.encode())

# Message ends with a single period.
endMessage = '\r\n.\r\n'
clientSocket.send(endMessage.encode())
recv5 = clientSocket.recv(1024).decode()
print("Response after sending message data:", recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
recv6 = clientSocket.recv(1024).decode()
print("Response after QUIT command:", recv6)
if recv6[:3] != '221':
    print('221 reply not received from server.')

clientSocket.close()