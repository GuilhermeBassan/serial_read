import json
import serial
import pymysql as sql
import os
"""
db = sql.connect(host = 'localhost',
		 user = 'root',
		 password = '',
		 db = '',
		 charset = '',
		 unix_socket = '',
		 cursorclass = pymysql.cursors.DictCursor)
"""
ser = serial.Serial(port = '/dev/ttyS0',		# Start Serial object in  port ttyS0
		    baudrate = 9600,			# Set baud rate at 9600bps
		    parity = serial.PARITY_NONE,	# Set parity to NONE
		    stopbits = serial.STOPBITS_ONE,	# Set stop bits to ONE
		    bytesize = serial.EIGHTBITS,	# Set byte size to EIGHT
		    timeout = 1)			# Set timeout to 1

packet = ""		# Empty string for the received packet
data = {}		# Empty dataset
data['Event'] = []	# Empty subset

def makeJson(id, serial, et, vd):
	data['Event'].append({				# Append items on the json
	     "ID" : id,					# Append packet ID
	     "Serial" : serial,				# Append packet serial
	     "Type" : et,				# Append packet event type
	     "VD" : vd})				# Append packet verifier digit
	with open("data.json", "a") as received:	# Creates or opens the json file
		json.dump(data, received, indent = 2)	# Dumps data into file
	data['Event'] = []

def breakPacket(pack):
	packetVD = ""				# Empty string for the verification digit
	packetET = ""				# Empty string for the event type
	packetID = ""				# Empty string for the message ID
	packetSerial = ""			# Empty string for the message serial
	for i in range (1, 4):			# Range of the Packet ID
		packetID += pack[i]		# Append ID info
	packetET = pack[4]			# Packet event type
	for i in range (5, len(pack) - 3):	# Range of the serial
		packetSerial += pack[i]		# Append serial info
	packetVD = pack[len(pack) - 3]		# Packet verifier digit
	return packetVD, packetET, packetID, packetSerial

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')

while True:

	x = ser.read()
	if x != b'\x00' and x != b'':			# If not NULL and not EMPTY
		packet += x.decode("utf-8", "ignore")	# Add byte to packet string
	if x == b'\x00':				# If the byte is null
		print(packet)				# Prints packet
		VD, ET, ID, SE = breakPacket(packet)
		makeJson(ID, SE, ET, VD)
		
