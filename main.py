from socket import *    

serverName = 'localhost'
serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.connect((serverName,serverPort))
serverSocket.close()