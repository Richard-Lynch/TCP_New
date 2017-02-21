from socket import *
import thread
import time
from random import randint


def grem():
    result = randint(0, 3)
    if result == 1:
        return str(result)
    else:
        return str(2)


def on_con(clientSocket, address):
    with open(fileName) as f:
        loop = 0
        not_end = True
        while not_end:
            c = f.read(2)
            if not c:
                print "End of file"
                not_end = False
                c = '2' + str(loop) + 'Closing Connection' + '2'
                int(loop)
                loop = loop + 1
                clientSocket.send(c)
                break
            print "Read two characters:", c
            list.insert(loop, c)
            print 'loop: ', str(loop), ' list[loop]: ', list[loop]
            # sentence = clientSocket.recv(1024)
            # print address, ' >> ', sentence
            # msg = raw_input('SERVER >> ')
            # capitalizedSentence = sentence.upper()
            if loop != 100:
                c = '1' + str(loop) + c + grem()
            else:
                c = '1' + str(loop) + c + '9'
            int(loop)
            loop = loop + 1
            clientSocket.send(c)
            time.sleep(1)
            # clientSocket.send(capitalizedSentence)
    clientSocket.close()


def on_ack(clientSocket, address):
    loop = True
    while loop:
        try:
            ack = clientSocket.recv(1024)
            print address, ' >> ', ack
            if ack[:4] == 'Nack':
                print 'In the resend function'
                print 'ack[-1:]', ack[-1:]
                ind = int(ack[-1:])
                print 'ind: ', ind
                print 'list[ind]: ', list[ind]
                remsg = '1' + str(ind) + list[ind] + str(grem())
                clientSocket.send(remsg)
            # msg = raw_input('SERVER >> ')
            # capitalizedSentence = sentence.upper()
            # clientSocket.send(msg)
            # clientSocket.send(capitalizedSentence)
        except:
            loop = False
            print 'Socket Closed.'
    clientSocket.close()


# def on_send(clientSocket,addr):
#     while True:
#         # clientSocket.close()
#         sentence = raw_input('Input lowercase sentance:')
#         serverSocket.send(sentence)
#         # modifiedSentence = serverSocket.recv(1024)
#         # print 'From Client:', modifiedSentence
#     serverSocket.close()

# def on_receive(clientSocket,address)
#     (clientsocket, address) = serversocket.accept()
#     ct = client_thread(clientsocket)
#     ct.run()
# random.seed
serverName = 'localhost'
serverPort = 12014
fileName = 'input.txt'
list = ['', '', '', '', '', '', '', '']
c = ''
# create a NET, streaming socket
serverSocket = socket(AF_INET, SOCK_STREAM)
# bind the socket to the host and port
serverSocket.bind((serverName, serverPort))
# become a server socket by listening - we will let 1 connection request
# occur before we refuse connections
serverSocket.listen(1)
print 'the server is ready to receive'

while True:
    # Establish connection with client.
    clientSocket, addr = serverSocket.accept()
    print 'Got connection from', addr
    thread.start_new_thread(on_con, (clientSocket, addr))
    thread.start_new_thread(on_ack, (clientSocket, addr))
serverSocket.close()
