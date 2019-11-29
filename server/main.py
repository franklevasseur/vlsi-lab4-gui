#!/home/francois/anaconda3/envs/vlsi-lab4/bin/python

from flask import Flask, send_from_directory, request, make_response, abort, jsonify
import serial
import serial.tools.list_ports

import os

print("##########################################################")
print("##########################################################")
print("##################### initializing... ####################")
print("##########################################################")
print("########################################################## \n")

print("##########################################################")
print("################## available ports are : #################")
print("########################################################## \n")

all_available_ports = serial.tools.list_ports.comports()
indexes = [i for i in range(len(all_available_ports))]

print("Available ports")
chosen_port = None
for i, (port, desc, hwid) in zip(indexes, sorted(all_available_ports)):
    print("#{}) {}: {} [{}]".format(i, port, desc, hwid))

print("Choose from available ports: {}".format(indexes))
user_port = input()
chosen_port_object = all_available_ports[int(user_port)]

print("Choose baud rate : ")
baudrate = input()

print("Chosen port is : {}".format(chosen_port_object[0]))
chosen_port = serial.Serial(chosen_port_object[0], baudrate=int(baudrate))

if chosen_port is None:
    print("\nNo UART connected...\n")
else :
    print("serial port is: " + str(chosen_port.is_open))
    if (chosen_port.is_open):
        print("Device connected")
    else:
        print("Device failed to connect")

print("##########################################################")
print("##########################################################")
print("##################### server starting ####################")
print("##########################################################")
print("########################################################## \n")

root_dir = os.getcwd()
print("current directory = {}".format(root_dir))

static_sources_dir = os.path.join(root_dir, 'build')
app = Flask(__name__, static_folder=static_sources_dir)

@app.route('/')
def hello_world():
    return send_from_directory(static_sources_dir, 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(static_sources_dir, filename)


@app.route('/debug', methods=['GET'])
def debug():
    return 'hello ;)'


@app.route('/pattern', methods=['POST'])
def post_pattern():

    if request.is_json:
        
        pattern = request.get_json()
        
        counter = 0
        buffer = [0,0,0,0,0,0,0,0]
        msgArray = []
        msgCount = 0
        for count in range(len(pattern)):
            if (counter < 8):
                buffer[counter] = pattern[count]
                counter = counter + 1
                if (counter > 7):
                    print(str(msgCount) + " - " + str(buffer))
                    str1 = ''.join(str(e) for e in buffer)
                    print("     Binary - " + str(str1))
                    print("     serial write value " + str(hex(int(str1, 2))))
                    t = int(str1, 2)
                    msgArray.append(t)
                    msgCount = msgCount + 1
                    counter = 0

        #permet d'envoyer les messages à l'envers pour accomoder la reconstruction
        for i in reversed(msgArray):
            packet = bytearray()
            print("     serial packet value " + str(i))
            packet.append(i)
            chosen_port.write(packet)

        print("\n")
        print("pattern : \n")
        print(pattern)
        print(len(pattern))
        print("\n")

        return "done" 

    abort(400)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
