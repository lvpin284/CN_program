import os
import socket


def handleRequest(clientSocket):
    # recv data
    recvData = clientSocket.recv(1024).decode("UTF-8")

    # find the fileName
    fileName = recvData.split()[1].split("//")[1].replace('/', '')
    print("fileName: " + fileName)
    filePath = "./" + fileName.split(":")[0].replace('.', '_')
    # judge if the file named "fileName" if existed
    try:
        file = open(filePath + "./index.html", 'rb')
        print("File is found in proxy server.")

    # if not exists, send req to get it
    except:
        print("File is not exist.\nSend request to server...")


def startProxy(port):
    proxyServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxyServerSocket.bind(("", port))
    proxyServerSocket.listen(0)
    while True:
        try:
            print("Proxy is waiting for connecting...")
            clientSocket, addr = proxyServerSocket.accept()
            print("Connect established")
            handleRequest(clientSocket)
            clientSocket.close()
        except Exception as e:
            print("error: {0}".format(e))
            break
    proxyServerSocket.close()


if __name__ == '__main__':
    port = int(input("choose a port number over 1024:"))
    startProxy(port)