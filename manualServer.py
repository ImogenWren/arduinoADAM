#!/usr/bin/env python3
'''
Manual Server

 Test server for websockets. Broadcast a JSON command following user input
https://realpython.com/python-sockets/
'''


# broadcastServer.py


import socket
import time
import acUnitGlobals as glbs
pack = glbs.jsonPack

#HOST = "127.0.0.1"
TESTHOST = "10.42.0.1"
HOST = TESTHOST
PORT = 65432

TEST_COMMAND = '{"cmd":"set", "V1":"open"}'

exceptions = 0

while(exceptions < 10):
    try:
        print(f"Starting acUnit Manual Test Server:\nListening on {HOST}:{PORT}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            while (1):
                s.listen()
                conn, addr = s.accept()
                with conn:
                    iteration = 0
                    while(conn):
                        print(f"Connected by {addr}")
                        try:
                            json_input = input(f"Please Enter JSON command in format: {TEST_COMMAND}\n\n")
                            if (json_input.lower() == "stop"):
                                exceptions = 11
                                break
                        except :
                            print("User Input Escaped - Restarting")
                            break
                        #print(iteration)
                        json_command = json_input.encode("UTF-8")
                        conn.sendall(json_command)
                        data = conn.recv(2048)
                        reply = int(data.decode())
                        print(f"Returned Value: {reply}")
                        if (reply == 0):
                            print("Command Successfully Sent")
                        else:
                            print(f"Error Returned Code: {data}")
                        #data_dic = pack.unpack_json(data)
                        #json_print = pack.dump_json()
                        #print(data_dic)
                        if not data:
                            print("No Data Rx - break")
                            break
                        iteration += 1
                        #time.sleep(1)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
        break
    except:
        print("Exception Handled, restarting")
        exceptions += 1
print("Program Quit")


