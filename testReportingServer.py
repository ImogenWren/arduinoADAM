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
TESTHOST = "10.42.0.1"
HOST = TESTHOST
PORT = 65433   ## command server is port 65432


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        #s.setblocking(False)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall("0")

        '''
        except ConnectionResetError:
        print("Caught Connection Reset Error: Likely Cause Client Drop Connection")
        print("Restarting")
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
        break
    except Exception as ex:  ## generic exception handler
        glbs.generic_exception_handler(ex)
        print("Exception Handled, restarting")
        exceptions += 1
        '''
print("Program Quit")








