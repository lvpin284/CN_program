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
        #responseMsg = file.readlines()
        #for i in range(0, len(responseMsg)):
           # clientSocket.sendall(responseMsg[i])
        responseMsg = file.read()
        clientSocket.sendall(responseMsg.encode("utf-8"))
        print("Send, done.")
    # if not exists, send req to get it
    except:
        print("File is not exist.\nSend request to server...")
        try:
            proxyClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverName = fileName.split(":")[0]
            proxyClientSocket.connect((serverName, 80))
            proxyClientSocket.sendall(recvData.encode("UTF-8"))
            responseMsg = b''
            while True:
                try:
                    data = proxyClientSocket.recv(4069)
                    if not data:
                        print("recieve end\n")
                        break
                    responseMsg += data
                except Exception as e:
                    print("Exception occurred:", str(e))
#            responseMsg = proxyClientSocket.recv(1026)
            print(len(responseMsg))
            print("File is found in server.")
            clientSocket.sendall(responseMsg)
            print("Send, done.")
            # cache
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            cache = open(filePath + "./index.html", 'w')
            cache.writelines(responseMsg.decode("UTF-8").replace('\r\n', '\n'))
            cache.close()
            print("Cache, done.")
        except Exception as e:
            print("Exception occurred:", str(e))
#        except:
#            print("Connect timeout.")


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
    while True:
        try:
            port = int(input("choose a port number over 1024:"))
        except ValueError:
            print("Please input an integer rather than {0}".format(type(port)))
            continue
        else:
            if port <= 1024:
                print("Please input an integer greater than 1024")
                continue
            else:
                break
    startProxy(port)