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
            list1.insert(loop, c)
            print 'loop: ', str(loop), ' list1[loop]: ', list1[loop]
            temp = new Frame()
            temp.setSeq(loop)
            temp.addPayload(list1[loop])
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
                print 'list1[ind]: ', list1[ind]
                remsg = '1' + str(ind) + list1[ind] + str(grem())
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
list1 = ['', '', '', '', '', '', '', '']
c = ''
# create a NET, streaming socket
serverSocket = socket(AF_INET, SOCK_STREAM)
# bind the socket to the host and port
serverSocket.bind((serverName, serverPort))
# become a server socket by list1ening - we will let 1 connection request
# occur before we refuse connections
serverSocket.list1en(1)
print 'the server is ready to receive'

while True:
    # Establish connection with client.
    clientSocket, addr = serverSocket.accept()
    print 'Got connection from', addr
    thread.start_new_thread(on_con, (clientSocket, addr))
    thread.start_new_thread(on_ack, (clientSocket, addr))
serverSocket.close()

class Frame:

    def __init__(self):  # any intneral methods needs to start with self or it will be complelty public
        # self.chars = []     #0=start 1=SeqNum 2=PayloadLength 3=PayLoad 4=Ack/Nack 5=Checksum
        # self.chars[0] = 's'
        # self.minLength = 13
        self.data = {
            'start': 's'
        }

    def __str__(self):
        return json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))

    def setSeq(self, SeqNum):
        # input SeqNum here, with min length of 4
        # self.data['SeqNum'] = "{0:0>4}".format(SeqNum)
        self.data['SeqNum'] = SeqNum

    def addPayload(self, payload):
        self.data['PayLoad'] = payload

    def calcLength(self):
        # payload length, min length 4
        # self.data['PayloadLength'] =
        # "{0:0>4}".format(len(self.data['PayLoad'])) #probs need to typecase
        # this
        self.data['PayloadLength'] = len(self.data['PayLoad'])

    def calcSum(self):
        # calc checksum here, with min length of 4
        self.data['checksum'] = 0
        self.checksum = crc16.crc16xmodem(json.dump(self.data))
        self.data['checksum'] = self.checkSum

    def prepSend(self):
        self.calcLength()
        self.calcSum()
        self.data_string = json.dumps(self.data)
        return self.data_string

    def readFrame(self, data_string):
        self.data_string = data_string
        self.data = json.loads(self.data_string)

    def compCheckSum(self):
        # calc new checksum
        self.newCheckSum = self.data['checksum']
        self.data['checksum'] = 0
        self.checksum = crc16.crc16xmodem(json.dumps(self.data))
        if self.checkSum == self.newCheckSum:
            return True
        else:
            return False
