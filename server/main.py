#!/home/francois/anaconda3/envs/vlsi-lab4/bin/python

from flask import Flask, send_from_directory, request, make_response, abort, jsonify
import serial
import serial.tools.list_ports

import os

#variable set up port serial
BAUD_RATE = 9600

print("##########################################################")
print("##########################################################")
print("##################### initializing... ####################")
print("##########################################################")
print("########################################################## \n")

print("##########################################################")
print("################## available ports are : #################")
print("########################################################## \n")

all_available_ports = serial.tools.list_ports.comports()

print("Available ports")
chosen_port = None
for port, desc, hwid in sorted(all_available_ports):
    if desc.startswith("FT232R"):
        print(" - {}: {} [{}]       << this one\n".format(port, desc, hwid))
        #chosen_port = serial.Serial(port, baudrate=BAUD_RATE)
        break
    else:
        print(" - {}: {} [{}]\n".format(port, desc, hwid))

print("Choose from available ports")
user_port  = input()
if (len(user_port) >= 4):
    chosen_port = serial.Serial(user_port.upper(), baudrate=BAUD_RATE)

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
        msgCount = 0
        for count in range(len(pattern)):
            if (counter < 8):
                buffer[counter] = pattern[count]
                counter = counter + 1
                if (counter > 7):
                    print(str(msgCount) + " - " + str(buffer))
                    str1 = ''.join(str(e) for e in buffer)
                    print("     Binary - " + str(str1))
                    print("     serial write value " + str("0x%x" % int(str1, 2)))
                    t = chr(int(str1, 2))
                    chosen_port.write(str.encode(t))
                    msgCount = msgCount + 1
                    counter = 0
                


        print("\n")
        print("pattern : \n")
        print(pattern)
        print(len(pattern))
        print("\n")

        return "done" 

    abort(400)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
