from socket import *
import sys
import thread
import time
from random import randint
import crc16
import json


class Stack:

    def __init__(self):  # any intneral methods needs to start with self or it will be complelty public
        self.items = []

    def __str__(self):
        return str(self.items)

    def pop(self, position):
        if position != -1:
            return self.items.pop(position)

    def push(self, item):
        self.items.insert(0, item)

    def flush(self):
        self.items = []

    def length(self):
        return len(self.items)

    def peek(self):
        return self.items[0]


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
        self.data['checksum'] = crc16.crc16xmodem(str(self.data['PayLoad']))

    def prepSend(self, greml):
        self.calcLength()
        self.calcSum()
        self.data['checksum'] += greml
        return json.dumps(self.data)

    def readFrame(self, data_string):
        self.data = json.loads(data_string)

    def compCheckSum(self):
        # print "self.data['checksum']", self.data['checksum']
        self.tempCheckSum = self.data['checksum']

        self.data['checksum'] = crc16.crc16xmodem(str(self.data['PayLoad']))
        # print "self.data['checksum']", self.data['checksum']
        if self.data['checksum'] == self.tempCheckSum:
            return True
        else:
            return False

    def ack(self):
        # print "me:", self, "."
        if self.compCheckSum():
            print "acked: ", self.data['seqnum']
            if self.data['start'] == "e":
                print "at the end"
                loop = False
            self.data['PayLoad'] = ""
            self.data['start'] = "a"
            clientSocket.send(json.dumps(self.data))
            
            return True
        else:
            print "nacked: ", self.data['seqnum']
            self.data['start'] = "n"
            clientSocket.send(json.dumps(self.data))
            return False

serverName = 'localhost'
serverPort = 12012
fileName = "outputFile.txt"
print 'Checking crc test', crc16.crc16xmodem('Hello, World!')
clientSocket = socket(AF_INET, SOCK_STREAM)  # create client socket
clientSocket.connect((serverName, serverPort))  # connect to the server
print 'Client has successfully connected to server'
# thread.start_new_thread(onRec, (clientSocket, addr))
# thread.start_new_thread(writeFromBuffer, (clientSocket, addr))
loop = True
next_ack = 0
min_buff = 0
buff_index = 0
buff_size = 5
buff = []
with open(fileName, 'w') as f:
    # f = open(fileName, 'r+')
    #  open(fileName) as f:
    while loop:
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
            # sys.stdout.write("sys:")
            # sys.stdout.write(sentence[i:j])
            # sys.stdout.write(".\n")
            # convert the string to the data
            buff[buff_index].readFrame(sentence[i:j])

            print "server >>", buff[buff_index]
            buff_index += 1
            sentence = sentence[j:]  # shorten the string
        # after reading all the packets received
        # print "next_ack: ", next_ack
        starting_pos = 0
        while starting_pos < buff_index:
            # print "x: ",buff[starting_pos].data['seqnum']
            x = (buff[starting_pos].data['seqnum'])
            if x == next_ack:  # if the frame being checked is the next to be acked
                # print "matched buff:", buff[starting_pos], "."
                if buff[starting_pos].ack():  # then ack
                    tstr = buff[starting_pos].data['PayLoad']
                    f.write(tstr)
                    next_ack += 1  # increment the next ack
                    buff.pop(i)  # then pop the frame off the stack
                    buff_index -= 1  # reduce the number of items in the buffer
                    starting_pos = 0  # start you search of the buffer again

                    break

            # if the frame being checked should already have been acked
            # elif x < next_ack:
            #     buff[starting_pos].ack()  # then ack
            #     buff.pop(i)  # then pop the frame off the stack
            #     buff_index -= 1  # reduce the number of items in the buffer
            #     starting_pos = 0  # start you search of the buffer again
            #     break

            else:
                starting_pos += 1  # otherwise check the next item in the buffer     
    clientSocket.close()  # when we leave the loop close the socket
