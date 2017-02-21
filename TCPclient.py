from socket import *    
import thread
import crc16
import json

serverName = 'localhost'
serverPort = 12014
clientSocket = socket(AF_INET, SOCK_STREAM) #create client socket
clientSocket.connect((serverName,serverPort)) #connect to the server
print 'Checking crc test', crc16.crc16xmodem('Hello, World!')
print 'Client has successfully connected to server'
loop = True
next_ack = 0
min_buff = 0
max_buff = 0
buff_size = 5
while loop:
    sentence = clientSocket.recv(1024)  #receive packets
    while len(sentence) > 0: # if there are any chars left in the string
        length = len(sentence)
        i = 0                # position in the string to start the frame
        while sentence[i] != '{':   #look for a '{'
            i += 1
            if(i >= length):        #if the string has been exhausted
                break
        j = i                 # where to start looking for the end of the frame
        quote = False
        while sentence[j] != '}' & quote == False:  #if you've found a closing bracket and you're not inside a quote
            if sentence[j] == '"':      #if inside a quote toggle quote bool
                quote = not quote
            j += 1                  #iterate
            if(j >= length):    # if string has been exhausted
                break
        j += 1          #incldue the closing }
        buff[max_buff] = Frame()    #add to the buffer
        buff[max_buff].readFrame(sentence[i:j]) #
        max_buff += 1
        sentence = sentence[j:]


    

    if sentence[0] == '1':  
        # calc checksum 
        print sentence[1], ' Ack? ', sentence[-1:] # print the checksum result
         
        if sentence[-1:] != '2': # if checksum doesnt match
            ack = 'Nack - ' + sentence[1] # send Nack with frame number
            clientSocket.send(ack)
        else:                    # if the checksum doesnt match
            ack = 'Ack - ' + sentence[1]    #send Ack with frame number
            clientSocket.send(ack)
            
    elif sentence[0] == '2':    #if at the end of the data stream
        ack = 'Ack - ' + sentence[1]    #ack the last packet
        clientSocket.send(ack)  
        loop = False #leave the loop
    print serverName, ' >> ', sentence[2:-1] #print the message from the server
clientSocket.close()    #when we leave the loop close the socket


class Frame:
    def __init__(self):     #any intneral methods needs to start with self or it will be complelty public
        # self.chars = []     #0=start 1=SeqNum 2=PayloadLength 3=PayLoad 4=Ack/Nack 5=Checksum
        # self.chars[0] = 's'
        # self.minLength = 13
        self.data = {
        'start': 's'
        }
        
    def __str__(self):
        return json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))

    def setSeq(self, SeqNum):
        #input SeqNum here, with min length of 4
        # self.data['SeqNum'] = "{0:0>4}".format(SeqNum)
        self.data['SeqNum'] = SeqNum

    def addPayload(self, payload):
        self.data['PayLoad'] = payload
    
    def calcLength(self):
        #payload length, min length 4
        # self.data['PayloadLength'] = "{0:0>4}".format(len(self.data['PayLoad'])) #probs need to typecase this
        self.data['PayloadLength'] = len(self.data['PayLoad'])
    
    def calcSum(self):
        #calc checksum here, with min length of 4
        self.checkSum = 1
        # self.data['checksum'] = "{0:0>4}".format(checkSum)
        self.data['checksum'] = self.checkSum
    
    def prepSend(self):
        self.data_string = json.dumps(self.data)
        return self.data_string
    
    def readFrame(self, data_string):
        self.data_string = data_string
        data = json.loads(self.data_string)

    def compCheckSum(self):
        # calc new checksum
        self.newCheckSum = 1
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

