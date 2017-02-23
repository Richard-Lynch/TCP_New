from socket import *
import thread
import time
from random import randint
import crc16
import json

serverName = 'localhost'
serverPort = 12014
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
while loop:
    sentence = clientSocket.recv(1024)  # receive packets
    while len(sentence) > 0:  # if there are any chars left in the string
        length = len(sentence)
        i = 0                # position in the string to start looking for the frame
        while sentence[i] != '{':  # look for a '{'
            if(i >= length):  # if the string has been exhausted
                break
            else:
                i += 1
        j = i                 # where to start looking for the end of the frame
        quote = False
        # if you've found a closing bracket and you're not inside a quote
        while sentence[j] != '}' & quote == False:
            if sentence[j] == '"':  # if inside a quote toggle quote bool
                quote = not quote
            
            if(j >= length):    # if string has been exhausted
                break
            else:
                j += 1  # iterate

        j += 1  # incldue the closing }
        buff[buff_index] = Frame()  # add to the buffer
        buff[buff_index].readFrame(sentence[i:j])   #convert the string to the data
        buff_index += 1                            
        sentence = sentence[j:]                     #shorten the string
    # after reading all the packets received

    while i < buff_index:
        if buff[i].data['SeqNum'] = next_ack:  # if the frame being checked is the next to be acked
            buff[i].ack()  # then ack
            next_ack += 1  # increment the next ack
            buff.pop(i)  # then pop the frame off the stack
            buff_index -= 1  # reduce the number of items in the buffer
            i = 0  # start you search of the buffer again

        # if the frame being checked should already have been acked
        elif buff[i].data['SeqNum'] < next_ack:
            buff[i].ack()  # then ack
            buff.pop(i)  # then pop the frame off the stack
            buff_index -= 1  # reduce the number of items in the buffer
            i = 0  # start you search of the buffer again

        else:
            i += 1  # otherwise check the next item in the buffer

    if sentence[0] == '1':
        # calc checksum
        print sentence[1], ' Ack? ', sentence[-1:]  # print the checksum result

        if sentence[-1:] != '2':  # if checksum doesnt match
            ack = 'Nack - ' + sentence[1]  # send Nack with frame number
            clientSocket.send(ack)
        else:                    # if the checksum doesnt match
            ack = 'Ack - ' + sentence[1]  # send Ack with frame number
            clientSocket.send(ack)

    elif sentence[0] == '2':  # if at the end of the data stream
        ack = 'Ack - ' + sentence[1]  # ack the last packet
        clientSocket.send(ack)
        loop = False  # leave the loop
    # print the message from the server
    print serverName, ' >> ', sentence[2:-1]
clientSocket.close()  # when we leave the loop close the socket


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
        self.checkSum = 1
        # self.data['checksum'] = "{0:0>4}".format(checkSum)
        self.data['checksum'] = self.checkSum

    def prepSend(self):
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

    '''
    def readFrame(self, string)
    
        chars[0] = string[0]
        if chars[0] == 's' :
            if len(string) >= self.minLength # min length
                chars[1] = string[2:5]
                if chars[1].isdecimal() :
                    chars[1] = int(chars[1])
                    chars[2] = string[6:7]
                    if chars[2].isdecimal() :
                        chars[2] = int(chars[2])
                        if len(string) - chars[2] == self.minLength : 
                            chars[3] = string[8:(8+chars[2])]
                            chars[4] = string[(8+chars[2]+1)]
                            chars[5] = string[-5:]
    
    while len(chars)>this.minLength:     #loop till the string is gone
        while chars[0] != 's':
            chars = chars[1:]   # chop off the first char
    '''
