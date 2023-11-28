#!/usr/bin/env python3
'''
Echo Server

 Test server for websockets. Accept and display incoming JSON formatted messages sent from a remote client
https://realpython.com/python-sockets/
'''


# broadcastServer.py


import socket
import time
import json
import acUnitGlobals as glbs
pack = glbs.jsonPack

#HOST = "127.0.0.1"
#TESTHOST = "10.42.0.1"
#HOST = TESTHOST
HOST = glbs.REPORT_SERVER_IP
PORT = glbs.COMMAND_PORT   ## command server is port 65432



while (1):
    try:
        print(f"Starting acUnit Reporting Test Server:\nListening on {HOST}:{PORT}")
        iteration = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                #s.setblocking(False)
                while True:
                    data = conn.recv(4096)
                    print(data)
                    data_dic = pack.unpack_json(data)
                    pack.print_json(data_dic)
                    if not data:
                        break
                    else:
                        success = "0"
                        conn.sendall(success.encode("UTF-8"))
                        print(f"iterations since last drop: {iteration}")
                        iteration +=1
    except ConnectionResetError:
        print("Caught Connection Reset Error: Likely Cause Client Drop Connection")
        print("Restarting")
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
        break
    except Exception as ex:  ## generic exception handler
        glbs.generic_exception_handler(ex)
        print("Exception Handled, restarting")
        #exceptions += 1
print("Program Quit")








