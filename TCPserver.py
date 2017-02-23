from socket import *
import thread
import time
import sys
from random import randint
import crc16
import json


class Frame:

    def __init__(self):  # any intneral methods needs to start with self or it will be complelty public
        # self.chars = []     #0=start 1=SeqNum 2=PayloadLength 3=PayLoad 4=Ack/Nack 5=Checksum
        # self.chars[0] = 's'
        # self.minLength = 13
        self.data = {
            'start': 's',
            'seqnum': 0,
            'PayLoad': 0,
            'PayloadLength': 0,
            'checksum': 0
        }
            # return json.dumps(self.data''', sort_keys=True, indent=4,
        # separators=(',', ': ')''')

    def __str__(self):
        return json.dumps(self.data)

    def setSeq(self, SeqNum):
        self.data['seqnum'] = SeqNum

    def addPayload(self, payload):
        self.data['PayLoad'] = payload

    def calcLength(self):
        self.data['PayloadLength'] = len(self.data['PayLoad'])

    def calcSum(self):
        # self.data['checksum'] = 0
        # self.data = json.loads(json.dumps(self.data))
        # self.data['checksum'] = crc16.crc16xmodem(json.dumps(self.data))
        self.data['checksum'] = crc16.crc16xmodem(str(self.data['PayLoad']))


    def prepSend(self, greml):
        self.calcLength()
        self.calcSum()
        self.data['checksum'] += greml
        return json.dumps(self.data)

    def readFrame(self, data_string):
        self.data = json.loads(data_string)

    def compCheckSum(self):
        print "self.data['checksum']", self.data['checksum']
        self.tempCheckSum = self.data['checksum']
    
        self.data['checksum'] = crc16.crc16xmodem(str(self.data['PayLoad']))
        print "self.data['checksum']", self.data['checksum']
        if self.data['checksum'] == self.tempCheckSum:
            return True
        else:
            return False

        # print "self.data['checksum']", self.data['checksum']
        # self.tempCheckSum = self.data['checksum']
        # self.data['checksum'] = 0
        # self.data['checksum'] = crc16.crc16xmodem(json.dumps(self.data))
        # print "self.data['checksum']", self.data['checksum']
        # if self.data['checksum'] == self.tempCheckSum:
        #     return True
        # else:
        #     return False


def grem():
    result = randint(0, 10)
    if result == 1:
        return result
    else:
        return 0


def on_con(clientSocket, address):
    with open(fileName) as f:
        loop = 0
        not_end = True
        while not_end:
            c = f.read(2)
            if not c:
                print "End of file"
                int(loop)
                temp = Frame()
                temp.setSeq(loop)
                temp.addPayload("")
                frame_buff.insert(0, temp)
                last_seq = loop
                cur_temp = temp.prepSend(grem())
                print "last sent >> ", cur_temp
                clientSocket.send(cur_temp)
                not_end = False
                # not_done = False
                break
            print "Read two characters:", c
            list1.insert(loop, c)
            # print 'loop: ', str(loop), ' list1[loop]: ', list1[loop]
            temp = Frame()
            temp.setSeq(loop)
            temp.addPayload(list1[loop])
            # temp.prepSend(0)
            frame_buff.insert(0, temp)
            # sentence = clientSocket.recv(1024)
            # print address, ' >> ', sentence
            # msg = raw_input('SERVER >> ')
            # capitalizedSentence = sentence.upper()

            int(loop)
            loop = loop + 1
            cur_temp = temp.prepSend(grem())
            print "sent >> ", cur_temp
            clientSocket.send(cur_temp)
            time.sleep(1)
            while RETRANS:
                fix = 1
            # clientSocket.send(capitalizedSentence)
    # clientSocket.close()


def on_ack(clientSocket, address):
    buff = []
    buff_index = 0
    while notDone:
        # print "test"
        sentence = clientSocket.recv(1024)  # receive packets
        while len(sentence) > 1:  # if there are any chars left in the string
            # print "sentence: ", sentence
            # sys.stdout.write(sentence)
            # print ""
            length = len(sentence)
            i = 0                # position in the string to start looking for the frame
            while sentence[i] != '{':  # look for a '{'
                if(i >= length - 1):  # if the string has been exhausted
                    break
                else:
                    i += 1
            j = i                 # where to start looking for the end of the frame
            # print "i: ", i
            quote = False
            # if you've found a closing bracket and you're not inside a quote
            while sentence[j] != '}' or quote == True:
                if sentence[j] == '"':  # if inside a quote toggle quote bool
                    quote = not quote

                if(j >= length - 1):    # if string has been exhausted
                    break
                else:
                    j += 1  # iterate

            j += 1  # incldue the closing }
            # print "j: ", j
            buff.insert(buff_index, Frame())  # add to the buffer
            # print "buff_index: ", buff_index
            # print "buff[buff_index]: ",  buff[buff_index]
            # convert the string to the data
            buff[buff_index].readFrame(sentence[i:j])
            print addr, ">>", buff[buff_index]
            buff_index += 1
            sentence = sentence[j:]  # shorten the string
        # after reading all the packets received

        # while i < buff_index:
        for i in range(0, len(buff) - 1):
            for j in (0, len(frame_buff) - 1):
                if buff[i].data['seqnum'] == frame_buff[j].data['seqnum']:
                    if buff[i].data['start'] == 'a':
                        RETRANS = False
                        buff.pop(i)
                        frame_buff.pop(j)
                        buff_index -= 1
                    elif buff[i].data['start'] == 'e':
                        notDone = False
                    else:
                        RETRANS = True
                        cur_temp = frame_buff[j].prepSend(grem())
                        print "resent >> ", cur_temp
                        clientSocket.send(cur_temp)
    clientSocket.close()
    print "closed ack socked?"


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
serverPort = 12011
fileName = 'input.txt'
list1 = ['', '', '', '', '', '', '', '']
c = ''
RETRANS = False
notDone = True

frame_buff = []
# create a NET, streaming socket
serverSocket = socket(AF_INET, SOCK_STREAM)
# bind the socket to the host and port
serverSocket.bind((serverName, serverPort))
# become a server socket by list1ening - we will let 1 connection request
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
