from socket import *
import sys
import thread
import time
from random import randint
import crc16
import json

fileName = "outputFile.txt"

# f = open(fileName, 'r+')

# f.write("hello")
# string = "world"
# f.write(string)

# f.close()

with open(fileName, 'w') as f1:
    f1.write("disk")


