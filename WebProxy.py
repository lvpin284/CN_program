import os
import socket

def handleRequest(clientSocket):
    # 接收客户端数据
    recvData = clientSocket.recv(1024).decode("UTF-8")

    # 提取文件名
    fileName = recvData.split()[1].split("//")[1].replace('/', '')
    print("fileName: " + fileName)
    filePath = "./" + fileName.split(":")[0].replace('.', '_')

    # 判断文件是否存在
    try:
        file = open(filePath + "./index.html", 'rb')
        print("File is found in proxy server.")
        responseMsg = file.read()
        clientSocket.sendall(responseMsg)
        print("Send, done.")
    except FileNotFoundError:
        print("File is not exist.\nSend request to server...")
        try:
            proxyClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverName = fileName.split(":")[0]
            proxyClientSocket.connect((serverName, 80))
            proxyClientSocket.sendall(recvData.encode("UTF-8"))

            responseMsg = b''  # 初始化为字节串
            while True:
                try:
                    data = proxyClientSocket.recv(4069)
                    if not data:
                        print("something\n")  # 在成功接收到数据时输出
                        break
                    responseMsg += data  # 连接字节串
                except Exception as e:
                    print("Exception occurred:", str(e))
                    # 其他处理异常的代码

            #responseMsg = proxyClientSocket.recv(4069)
            print("File is found in server.")
            clientSocket.sendall(responseMsg)
            print("Send, done.")

            # 缓存数据
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            cache = open(filePath + "./index.html", 'w', encoding='utf-8')
            cache.writelines(responseMsg.decode("UTF-8").replace('\r\n', '\n'))
            cache.close()
            print("Cache, done.")
        except Exception as e:
            print("Error during connection to server: ", e)


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
            if port <= 1024:
                print("Please input an integer greater than 1024")
                continue
            break
        except ValueError:
            print("Please input a valid integer for the port number.")
    startProxy(port)