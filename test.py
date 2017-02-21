import thread
import crc16
import json

print "hello!"

data = {
        'start': 's'
        }
data['seqnum'] = 1
data['payload'] = "oh }god what now"
data['payloadlength'] = len(data['payload'])
data['checksum'] = 1212

print "data: ", data

string = json.dumps(data)

print "string: ", string

new_data = json.loads(string)

print "new_data: ", new_data

print "new_data['seqnum']: ", new_data['seqnum']

print "new_data['payload']: ", new_data['payload']

print "string[0]: ", string[0] 

string2 = "richard"

print "string2", string2
print "string2[0:2]", string2[0:2]
print "string2[2:4]", string2[2:4]
