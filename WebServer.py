#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import socket
import sys
import threading


def handleRequest(tcpSocket):
	# 1. Receive request message from the client on connection socket
	# 2. Extract the path of the requested object from the message (second part of the HTTP header)
	# 3. Read the corresponding file from disk
	# 4. Store in temporary buffer
	# 5. Send the correct HTTP response error
	# 6. Send the content of the file to the socket
	# 7. Close the connection socket 
	pass # Remove/replace when function is complete

def startServer(serverAddress, serverPort):
	# 1. Create server socket
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# 2. Bind the server socket to server address and server port
	serverSocket.bind((serverAddress, serverPort))
	# 3. Continuously listen for connections to server socket
	serverSocket.listen(0)
	# 4. When a connection is accepted, call handleRequest function, passing new connection socket (see https://docs.python.org/3/library/socket.html#socket.socket.accept)
	while True:
		try:
			print("wait for connecting...")
			print("while true")
			tcpSocket, clientAddr = serverSocket.accept()
			print("one connection is established, ", end="")
			print("address is: %s" % str(clientAddr))
			handleThread = threading.Thread(target=handleRequest, args=(tcpSocket,))
			handleThread.start()
		except Exception as err:
			print(err)
			break
	# 5. Close server socket
	serverSocket.close()
	pass # Remove/replace when function is complete

if __name__ == '__main__':
    while True:
        try:
            hostPort = int(input("Input the port you want: "))
            startServer("", hostPort)
            break
        except Exception as e:
            print(e)
            continue

#startServer("", 8000)
