from digi.xbee.devices import XBeeDevice
import requests
import json
import os

'''Esto es para el bote, el bote envia a la estacion cada 500ms'''
#****************************************************************************************#
# Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyUSB1"
# Replace with the baud rate of your local module.
BAUD_RATE = 9600
#REMOTE_NODE_ID = "vtecstation" #El nodo con el que se quiere comunicar.
REMOTE_NODE_ID = "vtecboat"
#****************************************************************************************#

os.environ['NO_PROXY'] = '127.0.0.1'
local_address = 'http://127.0.0.1:5000/'

def send_xbee_instruction_to_server(instruction):
	r = requests.get(local_address+instruction)
	print(r.content)

def check_instruction(message):
	if message == 'AutonomousNavigation':
		send_xbee_instruction_to_server('AutonomousNavigation')
	elif message == 'FindThePath':
		send_xbee_instruction_to_server('FindThePath')
	elif message == 'SpeedChallenge':
		send_xbee_instruction_to_server('SpeedChallenge')
	elif message == 'RaiseTheFlag':
		send_xbee_instruction_to_server('RaiseTheFlag')
	elif message == 'AutomatedDocking':
		send_xbee_instruction_to_server('AutomatedDocking')
	elif message == 'GPSNavigation':
		send_xbee_instruction_to_server('GPSNavigation')
	elif message == 'Teleop':
		send_xbee_instruction_to_server('Teleop')

def read_xbee_data():
    print(" +-------------------------------------------------+")
    print(" |                       Bote                      |")
    print(" +-------------------------------------------------+\n")
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()
        device.flush_queues()

        print("Waiting conversation...\n")
        
        #Variable to stop the conversation 
        commActive = True

        while commActive :

            #Read data and chek if something has been received 
            xbee_message = device.read_data()
            if xbee_message is not None:
                
                #Print the message and 
                message = xbee_message.data.decode()
                print("Received Message: " , message)
                
                ##If the receive message is an instruction
                ##Send the instruction to the server.
                check_instruction(message)

                #if it's different than exit continue listening
                if xbee_message.data.decode() == 'exit':
                    commActive = False

    #If the device is not closed, close it.
    finally:
        if device is not None and device.is_open():
            device.close()

if __name__ == '__main__':
    read_xbee_data()
