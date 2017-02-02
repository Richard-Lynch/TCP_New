from socket import *
serverName = 'localhost'
serverPort = 12000
while 1:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # clientSocket.close()
    clientSocket.connect(('',serverPort))
    sentence = raw_input('Input lowercase sentance:')
    clientSocket.send(sentence)
    modifiedSentence = clientSocket.recv(1024)
    print 'From Server:', modifiedSentence
    clientSocket.close()