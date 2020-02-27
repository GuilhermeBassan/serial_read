import json	# Import json library
import serial	# Import serial library

ser = serial.Serial(port = '/dev/ttyS0',		# Start Serial object in  port ttyS0
		    baudrate = 9600,			# Set baud rate at 9600bps
		    parity = serial.PARITY_NONE,	# Set parity to NONE
		    stopbits = serial.STOPBITS_ONE,	# Set stop bits to ONE
		    bytesize = serial.EIGHTBITS,	# Set byte size to EIGHT
		    timeout = 1)			# Set timeout to 1

packet = ""		# Empty string for the received packet
packetVD = ""		# Empty string for the verification digit
packetET = ""		# Empty string for the event type
packetID = ""		# Empty string for the message ID
packetSerial = ""	# Empty string for the message serial

data = {}		# Empty dataset
data['Eventos'] = []	# Empty subset

while True:	# Infinite loop

	x = ser.read()	# Read received byte

	if x != b'\x00' and x != b'':			# If not NULL and not EMPTY
		packet += x.decode("utf-8", "ignore")	# Add byte to packet string
	if x == b'\x00':				# If the byte is null
		print(packet)				# Prints packet

		for i in range (1, 4):			# Range of the Packet ID
			packetID += packet[i]		# Append ID info
		packetET = packet[4]			# Packet event type
		for i in range (5, len(packet) - 3):	# Range of the serial
			packetSerial += packet[i]	# Append serial info
		packetVD = packet[len(packet) - 3]	# Packet verifier digit

		print("ID =", packetID,		# Print ID and
		      "Serial =", packetSerial,	# Print serial
		      "Tipo =", packetET,	# Print event type
		      "DV =", packetVD)		# Print verifier digit

		data['Eventos'].append({			# Append items on the json
		     "ID" : packetID,				# Append packet ID
		     "Serial" : packetSerial,			# Append packet serial
		     "Tipo" : packetET,				# Append packet event type
		     "DV" : packetVD})				# Append packet verifier digit
		with open("data.json", "a") as received:	# Creates or opens the json file
			json.dump(data, received, indent = 4)	# Dumps data into file

		packet = ""		# Erase packet content
		packetID = ""		# Erase packet ID content
		packetVD = ""		# Erase packet verifier digit
		packetET = ""		# Erase packet event type
		packetSerial = ""	# Erase packetSerial content
		data['Eventos'] = []	# Erase event subset

